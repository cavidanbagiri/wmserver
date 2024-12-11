from statistics import quantiles

from sqlalchemy import select, text, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.responses import JSONResponse
from fastapi import HTTPException

from db.setup import SessionLocal

from models.material_code_model import MaterialCodeModel
from models.material_type_model import MaterialTypeModel
from models.project_model import ProjectModel
from models.stock_model import StockModel
from models.warehouse_model import WarehouseModel
from models.area_model import AreaModel, UnusableMaterialModel, ServiceMaterialModel



class AreaRepository:

    def __init__(self, db: AsyncSession):
        self.db = None

class FetchAreaRepository(AreaRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def fetch(self, user_info):

        async with SessionLocal() as session:

            query = ''
            if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
                pass
            else:
                query = f'areas.project_id = {user_info.get('project')}'

            data = await session.execute(select(AreaModel, StockModel)
                                         .options(joinedload(AreaModel.stock))
                                         .options(joinedload(AreaModel.group))
                                         .options(joinedload(StockModel.warehouse_materials))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_code, MaterialCodeModel.material_description)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                         .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name))
                                        ).filter(text(query)))

            temp = data.unique().scalars().fetchall()
            return temp

class FilterAreaRepository(AreaRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def filter(self, queries, user_info):

        async with SessionLocal() as session:
            query = self.__create_query(queries, user_info).strip()

            if len(query):
                data = await session.execute(select(AreaModel, StockModel)
                                             .options(joinedload(AreaModel.stock))
                                             .options(joinedload(AreaModel.group))
                                             # .options(joinedload(StockModel.warehouse_materials))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_code,MaterialCodeModel.material_description)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                             .filter(text(query)))

            temp = data.unique().scalars().fetchall()
            return temp

    def __create_query(self, queries: dict, user_info) -> str:
        if user_info.get('is_admin') == True or user_info.get('status_code') == '1000':
            del queries['project_id']
        else:
            queries['areas.project_id'] = user_info.get('project')
        cond = ''
        for key, value in queries.items():
            if value:
                if key == 'material_name':
                    cond += f" warehouse_materials_1.{key} ILIKE '%{value}%' and"
                elif key == 'created_at':
                    cond += f" areas.{key}::date = '{value}' and"
                else:
                    cond += f" {key}='{value}' and "
        cond = cond[:len(cond) - 4]
        return cond

class GetDataByIdRepository(AreaRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_data_by_id(self, id:int):
        async with SessionLocal() as session:
            data = await session.execute(select(AreaModel).filter(AreaModel.id == id))
            temp = data.scalars().first()
            return temp

class UpdateAreaRepository(AreaRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def update(self, update_data: dict, user_info):
        async with SessionLocal() as session:
            await session.execute(update(AreaModel).where(AreaModel.id == update_data.get('id')).values(
                card_number = update_data.get('card_number'),
                username = update_data.get('username')
            ))

            await  session.commit()
            data = await session.execute(select(AreaModel, StockModel)
                                  .options(joinedload(AreaModel.stock))
                                  .options(joinedload(AreaModel.group))
                                  .options(joinedload(StockModel.warehouse_materials))
                                  .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_code,MaterialCodeModel.material_description)))
                                  .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                  .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                  .filter(AreaModel.id == update_data.get('id')))

            temp = data.scalars().first()
            return {
                'msg': 'Successfully Updated',
                'data': temp
            }

class ReturnAmountRepository(AreaRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def return_amount(self, return_data: dict, user_info):
        async with SessionLocal() as session:
            data = await session.execute(select(AreaModel).filter(AreaModel.id == return_data.get('id')))
            temp = data.scalars().first()

            if temp.quantity < float(return_data.get('return_amount')):
                raise HTTPException(status_code=400, detail="Entering amount can't be greater than leftover")
            else:

                # 1 - Update Area Model Quantity
                await session.execute(update(AreaModel).where(AreaModel.id == return_data.get('id')).values(
                    quantity = AreaModel.quantity - float(return_data.get('return_amount'))
                ))

                # 2 - Update Stock Model Leftover
                await session.execute(update(StockModel).where(StockModel.id == temp.stock_id).values(
                    leftover=StockModel.leftover + float(return_data.get('return_amount'))
                ))

                await  session.commit()
                data = await session.execute(select(AreaModel, StockModel)
                                             .options(joinedload(AreaModel.stock))
                                             .options(joinedload(AreaModel.group))
                                             .options(joinedload(StockModel.warehouse_materials))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_code).load_only(MaterialCodeModel.material_code,MaterialCodeModel.material_description)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.material_type).load_only(MaterialTypeModel.name)))
                                             .options(joinedload(StockModel.warehouse_materials).options(joinedload(WarehouseModel.project).load_only(ProjectModel.project_name)))
                                             .filter(AreaModel.id == return_data.get('id')))

                temp = data.scalars().first()
                return {
                    'msg': 'Successfully Updated',
                    'data': temp
                }