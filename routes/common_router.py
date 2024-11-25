
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

# from constants.messages import error_messages
from constants.messages import * 

# Import setup db
from db.setup import get_db

# Import SqlAlchemy functions
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

# Import Schemas
from schemas.common_schemas import CreateMaterialCodeSchema, GetMaterialCodeSchema, CreateProjectSchema, \
    GetProjectSchema, GetCompanySchema, CreateCompanySchema, GetOrderedSchema, CreateOrderedSchema, GetGroupSchema, \
    CreateGroupSchema, GetMaterialTypeSchema, CreateMaterialTypeSchema

# Import Repositories
from repositories.common_repository import MaterialCodeRepository, ProjectRepository, CompanyRepository, \
    GroupRepository, OrderedRepository, MaterialTypeRepository

# Import Token Verify Class
from dependecies.authorization import TokenVerifyMiddleware

router = APIRouter()


#########################################################                   Group Routers
# Checked
@router.get('/groups', status_code=200, response_model=List[GetGroupSchema])
async def fetch_groups(db: AsyncSession = Depends(get_db)):
    repository = GroupRepository(db)
    data = await repository.fetch()
    return data

# Checked
@router.post('/groups/add', status_code=201, response_model=GetGroupSchema)
async def create_group(group_data: CreateGroupSchema, db:AsyncSession = Depends(get_db),
                       user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = GroupRepository(db)
        try:
            data = await repository.create(group_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})
###################################################################################################



#########################################################                   Company Routers
# Checked
@router.get('/companies', status_code=200, response_model=List[GetCompanySchema])
async def fetch_company(db: AsyncSession = Depends(get_db)):
    repository = CompanyRepository(db)
    data = await repository.fetch()
    return data


# Checked
@router.post('/companies/add', status_code=201, response_model=GetCompanySchema)
async def crete_company(company_data: CreateCompanySchema, db: AsyncSession = Depends(get_db),
                         user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = CompanyRepository(db)
        try:
            data = await repository.create(company_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})


# Checked
@router.get('/companies/filter', status_code=201, response_model=List[GetCompanySchema], dependencies=[Depends(TokenVerifyMiddleware.verify_access_token)])
async def filter_company(company_name: Union[str, None]=None, db: AsyncSession = Depends(get_db),):
    repository = CompanyRepository(db)
    try:
        data = await repository.filter(company_name)
        return data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})

###################################################################################################



#########################################################                   Ordered Routers

# Checked
@router.get('/ordereds', status_code=200)
async def fetch_ordereds(db: AsyncSession = Depends(get_db)):
    repository = OrderedRepository(db)
    data = await repository.fetch()
    return data

# Checked
@router.post('/ordereds/add', status_code=201)
async def create_ordered(ordered_data: CreateOrderedSchema, db:AsyncSession = Depends(get_db),
                         user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = OrderedRepository(db)
        try:
            data = await repository.create(ordered_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})

# Checked
@router.get('/ordereds/filter', status_code=201, dependencies=[Depends(TokenVerifyMiddleware.verify_access_token)])
async def filter_ordered(ordered: Union[str, None]=None, db: AsyncSession = Depends(get_db),):
    repository = OrderedRepository(db)
    try:
        data = await repository.filter(ordered)
        return data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})

###################################################################################################


#########################################################                   Project Routers

# Checked
@router.get('/projects', status_code=200, response_model=List[GetProjectSchema])
async def fetch_project(db: AsyncSession = Depends(get_db)):
    repository = ProjectRepository(db)
    data = await repository.fetch()
    return data

# Checked
@router.post('/projects/add', status_code=201, response_model=GetProjectSchema)
async def create_project(create_project_data: CreateProjectSchema, db: AsyncSession = Depends(get_db),
                         user_info=Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin']:
        repository = ProjectRepository(db)
        try:
            data = await repository.create(create_project_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message': ADMIN_AUTHORIZATION_ERROR})

###################################################################################################


#########################################################                   Material Code Routers

# Checked
@router.get("/materialcodes", status_code=200, response_model=List[GetMaterialCodeSchema])
async def fetch_material_code(db: AsyncSession = Depends(get_db)):
    repository = MaterialCodeRepository(db)
    data = await repository.fetch()
    return data

# Checked
@router.get('/materialcodes/filter', status_code=200, response_model=List[GetMaterialCodeSchema])
async def filter_materialcodes(value: str, db:AsyncSession = Depends(get_db)):
    repository = MaterialCodeRepository(db)
    data = await repository.filter(value)
    return data

# Checked
@router.get("/materialcodes/{materialcode_id}", status_code=200, response_model=GetMaterialCodeSchema)
async def get_material_code_byid(materialcode_id: int, db: AsyncSession = Depends(get_db)):
    repository = MaterialCodeRepository(db)
    data = await repository.get_byid(materialcode_id)
    if not data:
        return JSONResponse(status_code=404, content={"message": "MaterialCode not found"})
    return data


# Checked
@router.post("/materialcodes/add", status_code=201, response_model=GetMaterialCodeSchema)
async def create_material_code(material_code_data : CreateMaterialCodeSchema , db: AsyncSession = Depends(get_db),
                               user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000'or user_info.get('status_code') == '10001':
        repository = MaterialCodeRepository(db)
        try:
            data = await repository.create(material_code_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})

###################################################################################################



#########################################################                   Material Type Routers

# Checked
@router.get('/materialtypes', status_code=200, response_model=List[GetMaterialTypeSchema])
async def fetch_material_types(db: AsyncSession = Depends(get_db)):
    repository = MaterialTypeRepository(db)
    data = await repository.fetch()
    return data


# Checked
@router.post('/materialtypes/add', status_code=200, response_model=GetMaterialTypeSchema)
async def create_material_types(material_type_data: CreateMaterialTypeSchema, db: AsyncSession = Depends(get_db),
                                user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info['is_admin'] or user_info.get('status_code') == '10000' or user_info.get('status_code') == '10001':
        repository = MaterialTypeRepository(db)
        try:
            data = await repository.create(material_type_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})
    else:
        return JSONResponse(status_code=403, content={'message':USER_AUTHORIZATION_ERROR})

