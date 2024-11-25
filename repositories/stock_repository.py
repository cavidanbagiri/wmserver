
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql import alias

from db.setup import SessionLocal
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

        print(f'coming filter user {user_info}')
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