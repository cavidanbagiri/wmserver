
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db.setup import get_db
from dependecies.authorization import TokenVerifyMiddleware

# Import Repository
from repositories.stock_repository import FetchStockRepository

router = APIRouter()


@router.get('/fetch', status_code=200)
async def fetch(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    repository = FetchStockRepository(db)
    data = await repository.fetch(user_info)
    return data