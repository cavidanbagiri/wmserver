import asyncio
import os
import uuid
from io import BytesIO
from typing import List, Union

from fastapi import HTTPException

from constants.messages import USER_AUTHORIZATION_ERROR
from db.setup import SessionLocal

# Import SqlAlchemy
from sqlalchemy.orm import joinedload
from sqlalchemy import text, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.certpass_model import CertPassModels
# Import Models
from models.company_model import CompanyModel
from models.ordered_model import OrderedModel
from models.project_model import ProjectModel
from models.material_type_model import MaterialTypeModel
from models.material_code_model import MaterialCodeModel
from models.stock_model import StockModel
from models.user_model import UserModel
from models.warehouse_model import WarehouseModel
from schemas.stock_schemas import CreateStockSchema

# Import Schemas
from schemas.warehouse_schemas import CreateWarehouseSchema, UpdateWarehouseSchema, UpdateCertorPassportSchema
from utils.s3_yandex import s3


class WarehouseRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


class CreateWarehouseRepository(WarehouseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(self, create_warehouse_data: List[CreateWarehouseSchema], user_info):
        return_datas = []
        async with SessionLocal() as session:
            for i in create_warehouse_data:
                await asyncio.sleep(2)
                data = WarehouseModel(
                    document=i.document,
                    material_name=i.material_name,
                    quantity=i.quantity,
                    leftover=i.quantity,
                    unit=i.unit,
                    price=i.price,
                    currency=i.currency,
                    po=i.po,
                    certificate=i.certificate,
                    passport=i.passport,
                    project_id=user_info.get('project'),
                    created_by_id=user_info.get('id'),
                    ordered_id=i.ordered_id,
                    material_code_id=i.material_code_id,
                    material_type_id=i.material_type_id,
                    company_id=i.company_id,
                )
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return_datas.append(data)
        return return_datas


class FetchWarehouseRepository(WarehouseRepository):

    def __init__(self, db):
        super().__init__(db)

    async def fetch(self, user_info):
        async with SessionLocal() as session:
            query = ''
            if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
                pass
            else:
                query = f'warehouse_materials.project_id = {user_info.get('project')}'
            data = await session.execute(select(WarehouseModel)
                                    .options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name))
                                    .options(joinedload(WarehouseModel.created_by).load_only(UserModel.first_name).load_only(UserModel.last_name))
                                    .options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name, OrderedModel.last_name))
                                    .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description, MaterialCodeModel.material_code))
                                    .options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name))
                                    .options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name))
                                    .filter(text(query))
                                    )
            temp = data.scalars().all()
            return temp


class FilterWarehouseRepository(WarehouseRepository):

    def __init__(self, db):
        super().__init__(db)

    async def filter_query(self, queries: dict, user_info):
        async with SessionLocal() as session:
            query = self.__create_query(queries, user_info).strip()

            if len(query):

                data = await session.execute(select(WarehouseModel)
                                        .options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name))
                                        .options(joinedload(WarehouseModel.created_by).load_only(UserModel.first_name).load_only(UserModel.last_name))
                                        .options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name).load_only(OrderedModel.first_name, OrderedModel.last_name))
                                        .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description, MaterialCodeModel.material_code))
                                        .options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name))
                                        .options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name))
                                        .filter(text(query))
                                        )
            else:
                data = await session.execute(select(WarehouseModel)
                                        .options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name))
                                        .options(joinedload(WarehouseModel.created_by).load_only(UserModel.first_name).load_only(UserModel.last_name))
                                        .options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name).load_only(OrderedModel.last_name, OrderedModel.last_name))
                                        .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description, MaterialCodeModel.material_code))
                                        .options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name))
                                        .options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
        temp = data.scalars().all()
        return temp

    def __create_query(self, queries: dict, user_info) ->str:
        print(f'................................coming queries {queries}')
        if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
            del queries['project_id']
        else:
            queries['warehouse_materials.project_id'] = user_info.get('project')
        cond = ''
        for key, value in queries.items():
            if value:
                if key == 'material_name':
                    cond += f" warehouse_materials.{key} ILIKE '%{value}%' and"
                elif key == 'created_at':
                    cond += f" warehouse_materials.{key}::date = '{value}' and"
                else:
                    cond += f" {key}='{value}' and "
        cond = cond[:len(cond) - 4]
        return cond


class ProvideWarehouseToStockRepository(WarehouseRepository):

    def __init__(self, db):
        super().__init__(db)

    async def provide(self, stock_data: List[CreateStockSchema], user_info):

        async with SessionLocal() as session:

            # Find data by id
            data = await self._find_warehouse_rows(stock_data, user_info)

            # Check quantities
            await self._check_quantity(data, stock_data)

            # Start a database transaction
            async with session.begin():
                await self._update_warehouse_quantity(data, stock_data, session)

            # Insert New Data to stock
            await session.commit()

            return {
                'message': 'Successfully provided',
                'data': await self._find_return_frontdata(stock_data, session)
            }

    async def _find_warehouse_rows(self, stock_data: List[CreateStockSchema], user_info) -> List[WarehouseModel]:
        async with SessionLocal() as session:
            return_data = []

            for row in stock_data:
                found = await session.execute(select(WarehouseModel).where(WarehouseModel.id == row.warehouse_id))
                temp = found.first()
                if temp[0].project_id != user_info.get('project'):
                    raise Exception(f'Can not provide to other project. Please write to admin')
                return_data.append(temp[0])
            return return_data

    async def _check_quantity(self, found_data, stock_data):
        for row in range(len(stock_data)):
            if stock_data[row].entered_amount > found_data[row].leftover:
                raise Exception(f'In {row} row, provide quantity greater than warehouse leftover amount. '
                                f'Leftover is : {found_data[row].leftover} and Entered amount is {stock_data[row].quantity}'
                                f' Please check it again')
            elif stock_data[row].entered_amount < 0:
                raise Exception(f'In {row} row, can be a negative amount')

    async def _update_warehouse_quantity(self, data: List[WarehouseModel], stock_data: List[CreateStockSchema], session):
        for row in range(len(stock_data)):
            await session.execute(update(WarehouseModel).where(WarehouseModel.id == data[row].id).values(
                leftover=WarehouseModel.leftover - stock_data[row].entered_amount))
            new_stock = StockModel(
                quantity=stock_data[row].entered_amount,
                leftover=stock_data[row].entered_amount,
                serial_number=stock_data[row].serial_number,
                material_id=stock_data[row].material_id,
                created_by_id=stock_data[row].created_by_id,
                warehouse_id=stock_data[row].warehouse_id
            )

            session.add(new_stock)

    async def _find_return_frontdata(self, stock_data: List[CreateStockSchema], session):
        returned_data = []
        for row in stock_data:
            found = await session.execute(select(WarehouseModel).where(WarehouseModel.id == row.warehouse_id))
            temp = found.first()
            find_dict = {
                'id': temp[0].id,
                'leftover': temp[0].leftover
            }
            returned_data.append(find_dict)
        return returned_data


class FetchSelectedItemsRepository(WarehouseRepository):

    def __init__(self, db):
        super().__init__(db)

    async def fetch_selected_items(self, items_list: Union[str, None] = None):
        async with SessionLocal() as session:
            datas = []
            for i in items_list:
                data = await session.execute(select(WarehouseModel)
                    .filter(WarehouseModel.id == int(i)))
                temp = data.scalars().first()
                datas.append(temp)
            return datas


class TypeCountRepository(WarehouseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def get_type_count(self, user_info):
        async with SessionLocal() as session:
            query = '''SELECT warehouse_materials.material_type_id, material_types.name, count(warehouse_materials.material_type_id) AS count 
                        FROM warehouse_materials 
                        left join material_types on material_types.id = warehouse_materials.material_type_id '''

            if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
                pass
            else:
                query += f' where warehouse_materials.project_id = {user_info.get("project")} '

            query += 'GROUP BY warehouse_materials.material_type_id, material_types.name'

            # Execute the query
            data = await session.execute(text(query))

            # Get values and convert to dict
            temp = data.mappings().all()
            result = [dict(i) for i in temp]

            total = 0
            for i in result:
                total += i.get('count')

            for i in result:
                i['type'] = i.get('name').title()
                i['count'] = round((i.get('count') / total) * 100)

            return result


class UpdateCertorPassportRepository(WarehouseRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def update_certor_passport_by_id(self, data: UpdateCertorPassportSchema):
        async with SessionLocal() as session:
            if data.key == 'certificate':
                await session.execute(update(WarehouseModel).where(WarehouseModel.id == data.id).values(
                    certificate = not data.value
                ))
            else:
                await session.execute(update(WarehouseModel).where(WarehouseModel.id == data.id).values(
                    passport = not data.value
                ))
            await session.commit()
            return_data = {
                'id': data.id,
                'key': data.key,
                'value': not data.value
            }
            return {"data": return_data, "msg":"Successfully updated"}


class GetWarehouseById(WarehouseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, warehouse_id):
        async with SessionLocal() as session:
            data = await session.execute(select(WarehouseModel).filter(WarehouseModel.id == warehouse_id)
                                         .options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name).load_only(OrderedModel.first_name,OrderedModel.last_name))
                                         .options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
            temp = data.mappings().first().WarehouseModel
            return temp


class UploadCertOrPassportRepository(WarehouseRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def upload_cert_or_passport(self, warehouse_id, file):

        # Upload Image To Cloud
        async with SessionLocal() as session:
            image_url = await self._upload_cert_passport_file_tocloud(file)
            new_data = CertPassModels(
                warehouse_id = warehouse_id,
                file_name = image_url.get('file_name'),
                link = image_url.get('url')
            )
            session.add(new_data)
            await session.commit()
        return { 'msg': "Successfully uploaded" }

    async def _upload_cert_passport_file_tocloud(self, file):
        if file:
            file_contents = await file.read()
            user_unique_id = uuid.uuid4()
            suffix = file.filename.split('.')[-1]
            file_path = str(user_unique_id)+'.'+suffix

            s3.upload_fileobj(BytesIO(file_contents), os.getenv('BUCKET_NAME'), 'certificates_and_passports/'+file_path)
            image_url = f'https://storage.yandexcloud.net/{os.getenv('BUCKET_NAME')}/certificates_and_passports/{file_path}'
            return {
                'url':image_url,
                'file_name': file.filename
            }


class FetchCertPassportRepository(WarehouseRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def fetch(self, warehouse_id):

        data = await self.db.execute(select(CertPassModels).filter(CertPassModels.warehouse_id == warehouse_id))
        temp = data.mappings().all()
        print(f'temp.................................. is {temp}')
        return temp


class UpdateWarehouseRepository(WarehouseRepository):
    def __init__(self, db):
        super().__init__(db)

    async def update(self, update_warehouse_data: UpdateWarehouseSchema, user_info):

        print('----------------------------------------------------------------------------')

        # Check if user is admin or authorization
        if (user_info['is_admin']
                or user_info.get('status_code') == '10000'
                or user_info.get('status_code') == '10001'
                or user_info.get('status_code') == '10001'
        ):

            # 1 Step, Check project is True
            await self._check_project(update_warehouse_data.id, user_info.get('project'))

            async with SessionLocal() as session:

                # 2 Step, Check quantity change or not
                result = await self._check_quantity_change(update_warehouse_data)

                # if quantity change
                if result:
                    data = await self._update_warehouse_data_with_quantity(update_warehouse_data, session)
                else:
                    data = await self._update_warehouse_data_without_quantity(update_warehouse_data, session)

                return data

        else:
            return HTTPException(status_code=403, detail={'message':USER_AUTHORIZATION_ERROR})

    # Checked
    async def _check_project(self, warehouse_id, user_project_id):
        repository = GetWarehouseById(db=self.db)
        temp = await repository.get_by_id(warehouse_id)
        if temp.project_id != user_project_id:
            raise HTTPException(status_code=403, detail={'message':USER_AUTHORIZATION_ERROR})

    # Checked
    async def _check_quantity_change(self, update_warehouse_data):
        repository = GetWarehouseById(db=self.db)
        temp = await repository.get_by_id(update_warehouse_data.id)
        if update_warehouse_data.quantity != temp.quantity:
            return True
        else:
            return False

    # Checked
    async def _update_warehouse_data_without_quantity(self, update_warehouse_data: UpdateWarehouseSchema, session):

        await session.execute(update(WarehouseModel).where(WarehouseModel.id == update_warehouse_data.id).values(
            document=update_warehouse_data.document,
            material_name=update_warehouse_data.material_name,
            quantity=update_warehouse_data.quantity,
            unit=update_warehouse_data.unit,
            price=update_warehouse_data.price,
            po=update_warehouse_data.po,
            company_id=update_warehouse_data.company_id,
            ordered_id=update_warehouse_data.ordered_id,
            material_type_id=update_warehouse_data.material_type_id
        ))

        await session.commit()
        repository = GetWarehouseById(db=self.db)
        temp = await repository.get_by_id(update_warehouse_data.id)
        return {
            'data': temp,
            'msg': 'Successfully updated'
        }

    # Checking
    async def _update_warehouse_data_with_quantity(self, update_warehouse_data: UpdateWarehouseSchema, session):

        # 1 - Check quantity less than or greater than leftover
        repository = GetWarehouseById(db=self.db)
        temp = await repository.get_by_id(update_warehouse_data.id)

        # 2 - Find Sum of stock data
        stock_sum = await self._find_stock_data(update_warehouse_data, session)

        # 3 - Check Entering Data with quantity and leftover

        # 3.1 - If entering data is less than leftover
        if update_warehouse_data.quantity < stock_sum:
            print('Entering data cant be less than enter 3.1 ------------------------------------------------')
            raise HTTPException(status_code=400, detail='Entering Quantity is less than leftover this is impossible')

        # 3.2 - If Entering Data greater than leftover and less than quantity and greater than leftover + stock
        elif update_warehouse_data.quantity < temp.quantity and update_warehouse_data.quantity >= stock_sum :
            print(f'Enter 3.2------------------------------------------------ {stock_sum}')
            await session.execute(update(WarehouseModel).where(WarehouseModel.id == update_warehouse_data.id).values(
                leftover = update_warehouse_data.quantity - stock_sum,
                quantity = update_warehouse_data.quantity, # 95
            ))
            await session.commit()
            repository = GetWarehouseById(db=self.db)
            temp = await repository.get_by_id(update_warehouse_data.id)
            return {
                'data': temp,
                'msg': 'Successfully updated'
            }

        # 3.3 - If Entering Data greater than leftover and less than quantity and less than leftover + stock
        elif update_warehouse_data.quantity > temp.quantity:
            print('Enter 3.3 ------------------------------------------------')
            await session.execute(update(WarehouseModel).where(WarehouseModel.id == update_warehouse_data.id).values(
                leftover=update_warehouse_data.quantity - stock_sum,
                quantity=update_warehouse_data.quantity,
            ))
            await session.commit()
            repository = GetWarehouseById(db=self.db)
            temp = await repository.get_by_id(update_warehouse_data.id)
            return {
                'data': temp,
                'msg': 'Successfully updated'
            }


        return {}

    # Checking
    async def _find_stock_data(self, update_warehouse_data: UpdateWarehouseSchema, session):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Start Find Stock ')
        total = 0
        data = await session.execute(select(StockModel).filter(StockModel.warehouse_id == update_warehouse_data.id))
        temp = data.mappings().all()
        for i in temp:
            print(f'each i >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {i.get('StockModel')}')
            total += i.get('StockModel').quantity

        print(f'........................ total is {total}')
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> End Find Stock ')
        return total