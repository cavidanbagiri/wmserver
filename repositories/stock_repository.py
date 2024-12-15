

from fastapi import HTTPException

from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.setup import SessionLocal

from models.area_model import AreaModel, UnusableMaterialModel, ServiceMaterialModel
from models.company_model import CompanyModel
from models.material_code_model import MaterialCodeModel
from models.material_type_model import MaterialTypeModel
from models.ordered_model import OrderedModel
from models.project_model import ProjectModel
from models.stock_model import StockModel
from models.warehouse_model import WarehouseModel


class StockRepository:

    def __init__(self, db):
        self.db = db

class FetchStockRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def fetch(self, user_info):

        async with SessionLocal() as session:

            query = ''
            if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
                pass
            else:
                query = f'warehouse_materials_1.project_id = {user_info.get('project')}'

            data = await session.execute(select(StockModel)
                                         .options(joinedload(StockModel.warehouse_materials)
                                         .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description,MaterialCodeModel.material_code)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name, OrderedModel.last_name)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                         .filter(text(query)))

            temp = data.scalars().fetchall()
            return temp


class FilterStockRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def filter(self, queries, user_info):
        async with SessionLocal() as session:
            query = self.__create_query(queries, user_info).strip()

            if len(query):

                data = await session.execute(select(StockModel)
                                             .options(joinedload(StockModel.warehouse_materials)
                                             .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description,MaterialCodeModel.material_code)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name, OrderedModel.last_name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                             .filter(text(query)))
            else:
                data = await session.execute(select(StockModel)
                                             .options(joinedload(StockModel.warehouse_materials)
                                             .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description,MaterialCodeModel.material_code)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name, OrderedModel.last_name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name))))

        temp = data.scalars().all()
        return temp

    def __create_query(self, queries: dict, user_info) -> str:
        if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
            del queries['project_id']
        else:
            queries['warehouse_materials_1.project_id'] = user_info.get('project')
        cond = ''
        for key, value in queries.items():
            if value:
                if key == 'material_name':
                    cond += f" warehouse_materials_1.{key} ILIKE '%{value}%' and"
                elif key == 'created_at':
                    cond += f" stocks.{key}::date = '{value}' and"
                else:
                    cond += f" {key}='{value}' and "
        cond = cond[:len(cond) - 4]
        return cond


class GetDataByIDS(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_data_by_ids(self, ids, user_info):
        return_datas = []
        async with SessionLocal() as session:
            for i in ids:
                data2 = await session.execute(select(StockModel)
                                .options(joinedload(StockModel.warehouse_materials)
                                .options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_description,MaterialCodeModel.material_code)))
                                .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.ordered).load_only(OrderedModel.first_name, OrderedModel.last_name)))
                                .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.company).load_only(CompanyModel.company_name)))
                                .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                .filter(StockModel.id == int(i)))
                temp = data2.scalars().first()
                return_datas.append(temp)
        return return_datas


class ProvideRepositories(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def provide(self, user_info, datas):
        async with SessionLocal() as session:
            count = 0
            for i in datas.get('data'):
                count+=1
                await self._check_quantity_by_id(int(i.get('stock_id')), float(i.get('quantity')), session, count)
                # Add Data To AreaModel
                new_data = AreaModel(
                    quantity = float(i.get('quantity')),
                    serial_number = i.get('serial_number'),
                    material_id = i.get('material_id'),
                    provide_type = i.get('provider_type'),
                    card_number = datas.get('card_number'),
                    username = datas.get('username'),
                    group_id = int(datas.get('group_id')),
                    stock_id = int(i.get('stock_id')),
                    created_by_id = int(user_info.get('id')),
                    project_id = int(user_info.get('project'))
                )
                session.add(new_data)
            await session.commit()
            data = {
                'msg': 'Successfully provided',
                'data': await self._find_return_frontdata(datas, session)
            }
            return data

    async def _check_quantity_by_id(self, stock_id:int, quantity: float, session, count):
        # 1 - Find Data
        data = await session.execute(select(StockModel).filter(StockModel.id == int(stock_id)))

        temp = data.scalars().first()
        if quantity > temp.leftover:
            raise HTTPException(status_code=400, detail=f'Entering quantity is greater than left over in {count} row')
        elif quantity <= 0:
            raise HTTPException(status_code=400, detail=f'entering quantity cant be negative or zero in {count} row')
        else:
            await session.execute(update(StockModel).where(StockModel.id == stock_id).values(leftover = StockModel.leftover - quantity))

    async def _find_return_frontdata(self, datas, session):
        returned_data = []
        for row in datas.get('data'):
            found = await session.execute(select(StockModel).where(StockModel.id == int(row.get('stock_id'))))
            temp = found.first()
            find_dict = {
                'id': temp[0].id,
                'leftover': temp[0].leftover
            }
            returned_data.append(find_dict)
        return returned_data


class GetStockByIdRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_stock_by_id(self,  stock_id:int):
        async with SessionLocal() as session:
            data = await session.execute(select(StockModel).options(joinedload(StockModel.warehouse_materials))
                                        .filter(StockModel.id == int(stock_id)))
            temp = data.scalars().first()
            return temp


class UpdateRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def update(self, data):
        async with SessionLocal() as session:
            await session.execute(update(StockModel).where(StockModel.id == data.get('id'))
                                         .values(serial_number=data.get('serial_number'), material_id=data.get('material_id')))
            await session.commit()
            data = await session.execute(select(StockModel).options(joinedload(StockModel.warehouse_materials))
                                         .filter(StockModel.id == int(data.get('id'))))
            temp = data.scalars().first()
            return {
                'msg':'Successfully Updated',
                'data': temp
            }


class SetUnusableRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.repository = GetStockByIdRepository(db)

    async def set_unusable(self, data: dict, user_info):
        async with SessionLocal() as session:

            temp = await self.repository.get_stock_by_id(int(data.get('stock_id')))
            if float(data.get("quantity")) <= temp.leftover:

                # 1 - Create new unusable row
                created_data = UnusableMaterialModel(
                    quantity = float(data.get('quantity')),
                    comment = data.get('comment'),
                    created_by_id = user_info.get('id'),
                    stock_id = data.get('stock_id'),
                    project_id = user_info.get('project')
                )
                session.add(created_data)

                # 2 - Update Stock Data
                await session.execute(update(StockModel).filter(StockModel.id == int(data.get('stock_id'))).values(leftover = StockModel.leftover - float(data.get('quantity'))))
                await session.commit()

                return {
                    'msg': 'Successfully Added',
                    'data': await self.repository.get_stock_by_id(int(data.get('stock_id')))
                }
            else:
                raise HTTPException(status_code=400, detail="Entering amount can't be greater than leftover")


class SetServiceRepository(StockRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.repository = GetStockByIdRepository(db)

    async def set_service(self, data: dict, user_info):
        async with SessionLocal() as session:

            temp = await self.repository.get_stock_by_id(int(data.get('stock_id')))
            if float(data.get("quantity")) <= temp.leftover:

                # 1 - Create new unsuable row
                created_data = ServiceMaterialModel(
                    quantity = float(data.get('quantity')),
                    comment = data.get('comment'),
                    created_by_id = user_info.get('id'),
                    stock_id = data.get('stock_id'),
                    project_id=user_info.get('project')
                )
                session.add(created_data)

                # 2 - Update Stock Data
                await session.execute(update(StockModel).filter(StockModel.id == int(data.get('stock_id'))).values(leftover = StockModel.leftover - float(data.get('quantity'))))
                await session.commit()

                # 3 - Return data back

                return {
                    'msg': 'Successfully Added',
                    'data': await self.repository.get_stock_by_id(int(data.get('stock_id')))
                }
            else:
                raise HTTPException(status_code=400, detail="Entering amount can't be greater than leftover")


class ReturnWarehouseRepository(StockRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.repository = GetStockByIdRepository(db)

    async def return_warehouse(self, data, user_info):
        async with SessionLocal() as session:

            # Find Data and check quantity
            temp = await self.repository.get_stock_by_id(int(data.get('stock_id')))
            if float(data.get('return_amount')) > temp.leftover:
                raise HTTPException(status_code=400, detail="Entering amount can't be greater than leftover")
            else:

                # 1 - Withdraw quantity from stock model
                await session.execute(update(StockModel).filter(StockModel.id == data.get('stock_id'))
                                      .values(leftover = StockModel.leftover - float(data.get('return_amount')),
                                              quantity = StockModel.quantity - float(data.get('return_amount'))))

                # 2 - Add withdraw quantity to warehouse
                await session.execute(update(WarehouseModel).filter(WarehouseModel.id == data.get('warehouse_id')).
                                      values(leftover = WarehouseModel.leftover + float(data.get('return_amount'))))

                await session.commit()

                # 3 - Return Back refreshing data

                return {
                    'msg': 'Successfully Returned',
                    'data': await self.repository.get_stock_by_id(int(data.get('stock_id')))
                }












