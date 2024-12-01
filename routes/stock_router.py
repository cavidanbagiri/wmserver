
import datetime


from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from constants.messages import USER_AUTHORIZATION_ERROR
from db.setup import get_db
from dependecies.authorization import TokenVerifyMiddleware

# Import Repository
from repositories.stock_repository import FetchStockRepository, FilterStockRepository, GetDataByIDS, \
    ProvideRepositories, GetStockByIdRepository, UpdateRepository
from schemas.area_schemas import CreateAreaSchema

router = APIRouter()

# Checked
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

# Used for getting datas with id, especially used in provide data to area
@router.post('/datas', status_code=201)
async def get_data_by_ids(ids: list[str], db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repositories = GetDataByIDS(db)
        data = await repositories.get_data_by_ids(ids, user_info)
        return data
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})



@router.post('/provide', status_code=201)
async def provide(datas: dict, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = ProvideRepositories(db)
        try:
            data = await repository.provide(user_info, datas)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})

    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})

@router.get('/{stock_id}', status_code=200)
async def update(stock_id:int, db:AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):
        repository = GetStockByIdRepository(db)
        try:
            data = await repository.get_stock_by_id(stock_id, user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=400, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})

@router.post('/update', status_code=201)
async def update(data: dict, db:AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):
        repository = UpdateRepository(db)
        try:
            data = await repository.update(data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=400, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})
