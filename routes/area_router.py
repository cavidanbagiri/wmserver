

import datetime

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from constants.messages import USER_AUTHORIZATION_ERROR
from db.setup import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from dependecies.authorization import TokenVerifyMiddleware
from repositories.area_repository import FetchAreaRepository, FilterAreaRepository, UpdateAreaRepository, \
    GetDataByIdRepository, ReturnAmountRepository, FetchUnusableMaterialsRepository, FetchServiceMaterialsRepository, \
    UnusableToStockRepository, ServiceToStockRepository

router = APIRouter()

@router.get('/fetch', status_code=200)
async def fetch(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):
        repository = FetchAreaRepository(db)
        try:
            data = await repository.fetch(user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.get('/fetchservicematerials', status_code=200)
async def fetch_service_materials(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = FetchServiceMaterialsRepository(db)
        try:
            data = await repository.fetch_service_materials(user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})



@router.get('/fetchunusablematerials', status_code=200)
async def fetch_unusable_materials(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = FetchUnusableMaterialsRepository(db)
        try:
            data = await repository.fetch_unusable_materials(user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.get('/filter', status_code=200)
async def filter(
        created_at: datetime.date | None = None,
        card_number: str | None = None,
        material_name: str | None = None,
        po: str | None = None,
        material_code_id: int | None = None,
        db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):
        queries = {
            'material_name': material_name,
            'po': po,
            'material_code_id': material_code_id,
            'created_at': created_at,
        }
        repository = FilterAreaRepository(db)
        try:
            data = await repository.filter(queries, user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.get('/{data_id}', status_code=200)
async def get_by_id(data_id: int, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = GetDataByIdRepository(db)
        try:
            data = await repository.get_data_by_id(data_id)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.post('/update', status_code=201)
async def update(update_data: dict, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = UpdateAreaRepository(db)
        try:
            data = await repository.update(update_data, user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.post('/return', status_code=201)
async def update(update_data: dict, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if (user_info['is_admin'] or
            user_info.get('status_code') == '10000' or
            user_info.get('status_code') == '10001' or
            user_info.get('status_code') == '10002'):

        repository = ReturnAmountRepository(db)
        try:
            data = await repository.return_amount(update_data, user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


@router.post('/unusabletostock', status_code=201)
async def unusable_to_stock(data: dict, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    repository = UnusableToStockRepository(db)
    try:
        data = await repository.unusable_to_stock(data, user_info)
        return data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})


@router.post('/servicetostock', status_code=201)
async def unusable_to_stock(data: dict, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    repository = ServiceToStockRepository(db)
    try:
        data = await repository.service_to_stock(data, user_info)
        return data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})