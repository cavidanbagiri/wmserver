import datetime
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse

from db.setup import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from constants.messages import *

# Import Schemas
from schemas.stock_schemas import CreateStockSchema
from schemas.warehouse_schemas import CreateWarehouseSchema, UpdateWarehouseSchema, UpdateCertorPassportSchema

# Import Repositories
from repositories.warehouse_repository import CreateWarehouseRepository, FilterWarehouseRepository, \
    ProvideWarehouseToStockRepository, UpdateWarehouseRepository, FetchWarehouseRepository, \
    FetchSelectedItemsRepository, TypeCountRepository, UpdateCertorPassportRepository, UploadCertOrPassportRepository, \
    FetchCertPassportRepository, GetWarehouseById

# Import Token Verify Class
from dependecies.authorization import TokenVerifyMiddleware

router = APIRouter()


# Checked
@router.get('/fetch')
async def fetch(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    repository = FetchWarehouseRepository(db)
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
    filter_warehouse_repository = FilterWarehouseRepository(db)
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
    data = await filter_warehouse_repository.filter_query(queries, user_info)
    return data


# Checked
@router.post('/fetchselecteditems')
async def fetch_selected_items(data: list[str, None] = None, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = FetchSelectedItemsRepository(db)
        try:
            data = await repository.fetch_selected_items(data)
            return data
        except Exception as e:
            return JSONResponse(status_code=201, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})



# Checked
@router.post('/create', status_code=201)
async def warehouse_create(warehouse_data: List[CreateWarehouseSchema], db: AsyncSession = Depends(get_db),
                           user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = CreateWarehouseRepository(db)
        try:
            data = await repository.create(warehouse_data, user_info)
            return JSONResponse(status_code=201, content={'message':"Material created successfully"})
        except Exception as e:
            return JSONResponse(status_code=404, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})


# Checked
@router.post('/provide', status_code=201)
async def provide_to_stock(stock_data: List[CreateStockSchema], db: AsyncSession = Depends(get_db),
                           user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    print(f'start {user_info}')
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = ProvideWarehouseToStockRepository(db)
        try:
            data = await repository.provide(stock_data, user_info)

            return data
        except Exception as e:
            return JSONResponse(status_code=404, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


# Checked
@router.get('/typecount/{project_id}', status_code=200)
async def getTypeCount(db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001' or user_info.get('status_code') == '1000':
        repository = TypeCountRepository(db)
        data = await repository.get_type_count(user_info)
        return data
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


# Checked
@router.post('/updatecertorpassportbyid', status_code=201)
async def update_certor_passport_by_id(data: UpdateCertorPassportSchema, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get(
            'status_code') == '10001' or user_info.get('status_code') == '1000':
        repository = UpdateCertorPassportRepository(db)
        try:
            data = await repository.update_certor_passport_by_id(data)
            return data
        except Exception as e:
            return JSONResponse(status_code=404, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


# Checked
@router.post('/uploadcertificateorpassport/{warehouse_id}', status_code=201)
async def upload_cert_or_passport(warehouse_id: int, file: UploadFile=File(...), db: AsyncSession = Depends(get_db),
                           user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001' or user_info.get('status_code') == '1000' :
        repository = UploadCertOrPassportRepository(db)
        try:
            data = await repository.upload_cert_or_passport(warehouse_id, file)
            return data
        except Exception as e:
            return JSONResponse(status_code=404, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})


# Checked
@router.get('/fetchcertificatesorpassport/{warehouse_id}', status_code=200)
async def fetch_cert_passport(warehouse_id: int, db: AsyncSession = Depends(get_db)):
    repository = FetchCertPassportRepository(db)
    try:
        data = await repository.fetch(warehouse_id)
        return data
    except Exception as e:
        print(f'exceptions ......................... is {e}')
        return JSONResponse(status_code=403, content={'message': 'Internal Server Error, Give an inform to admin'})


# Checked
@router.get('/{id}', status_code=200)
async def getDataById(id: int, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = GetWarehouseById(db)
        try:
            data = await repository.get_by_id(id)
            return data
        except Exception as e:
            return JSONResponse(status_code=404, content={'message': str(e)})
    else:
        return JSONResponse(status_code=403, content={'message': USER_AUTHORIZATION_ERROR})

# Checking
@router.post('/update', status_code=201)
async def update_warehouse(update_warehouse_data: UpdateWarehouseSchema, db: AsyncSession = Depends(get_db),
                           user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001' or user_info.get('status_code') == '10001':
        repository = UpdateWarehouseRepository(db)
        try:
            data = await repository.update(update_warehouse_data, user_info)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={'msg': str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})