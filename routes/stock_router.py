
import datetime

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db.setup import get_db
from dependecies.authorization import TokenVerifyMiddleware

# Import Repository
from repositories.stock_repository import FetchStockRepository, FilterStockRepository

router = APIRouter()


@router.get('/fetch', status_code=200)
async def fetch(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    repository = FetchStockRepository(db)
    data = await repository.fetch(user_info)
    return data

# Checked
@router.get('/filter')
async def filter_query(
        document: str | None = None,
        material_name: str | None = None,
        po: str | None = None,
        company_id: int | None = None,
        project_id: int | None = None,
        created_by_id: int | None = None,
        ordered_id: int | None = None,
        material_code_id: int | None = None,
        material_type_id: int | None = None,
        created_at: datetime.date | None = None,
        db: AsyncSession=Depends(get_db),
        user_info = Depends(TokenVerifyMiddleware.verify_access_token)
        ):
    filter_warehouse_repository = FilterStockRepository(db)
    queries = {
        'document': document,
        'material_name': material_name,
        'po': po,
        'project_id': project_id,
        'created_by_id': created_by_id,
        'ordered_id': ordered_id,
        'material_code_id': material_code_id,
        'material_type_id': material_type_id,
        'company_id': company_id,
        'created_at': created_at,
    }
    data = await filter_warehouse_repository.filter(queries, user_info)
    return data
