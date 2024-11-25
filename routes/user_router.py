
from typing import List, Annotated


from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile
from fastapi.responses import JSONResponse

# Import Sqlalchemy
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession

# Import Error Messages
from constants.messages import * 

# Import Setups
from db.setup import get_db

# Import Schemas
from schemas.user_schemas import GetUserSchema, CreateUserSchema, LoginUserSchema, GetUserStatusSchema, CreateUserStatusSchema

# Import Repository
from repositories.user_repository import UserLoginRepository, UserRegisterRepository, UserFetchRepository, \
    UserProfileImageRepository, UserStatusRepository

# Import Dependency Injection Methods for token
from dependecies.authorization import TokenVerifyMiddleware

router = APIRouter()

# Checked
@router.get("/", status_code=200, dependencies=[Depends(TokenVerifyMiddleware.verify_access_token)])
async def fetch_users(request: Request, db: AsyncSession = Depends(get_db),):
    repository = UserFetchRepository(db)
    data = await repository.fetch_users()
    return data


# Don't need async await operation
@router.get('/refresh', status_code=200)
async def refresh(request: Request, user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if user_info:
        return JSONResponse(status_code=200, content={'user': user_info})
    else:
        return None

# Checked
@router.post("/login", status_code=200)
async def login(login_data: LoginUserSchema, db: AsyncSession= Depends(get_db)):
    repository = UserLoginRepository(db)
    try:
        data = await repository.login(login_data.email, login_data.password)
        return data
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": str(e.detail)})


# Checking
@router.post('/uploadimg', status_code=201)
async def upload_img(request: Request, user_info: Annotated[dict, Depends(TokenVerifyMiddleware.verify_access_token) ],
                     db: AsyncSession = Depends(get_db), file: UploadFile=File(...)):
    repository = UserProfileImageRepository(db)
    try:
        url = await repository.upload_image(user_info, file)
        return JSONResponse(status_code=201, content={'message':'image added successfully', 'url':url})
    except HTTPException as e:
        return JSONResponse(status_code=404, content={"message": str(e.detail)})

# Checked
@router.post("/create", status_code=201, response_model=GetUserSchema)
async def create_users(user_data: CreateUserSchema , db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if(user_info['is_admin'] == True):
        repository = UserRegisterRepository(db)
        try:
            data = await repository.create_user(user_data)
            return data
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"message": str(e)})
    else:
        return JSONResponse(status_code=403, content={'message':ADMIN_AUTHORIZATION_ERROR})
        
# Checked
@router.get('/fetchuserstatus', status_code=200, dependencies=[Depends(TokenVerifyMiddleware.verify_access_token)])
async def fetch_user_status(db: AsyncSession = Depends(get_db)):
    repository = UserStatusRepository(db)
    data = await repository.fetch_user_status()
    return data

# Checked
@router.post('/adduserstatus', status_code=201)
async def add_user_status(user_status_data: CreateUserStatusSchema, db: AsyncSession = Depends(get_db), user_info = Depends(TokenVerifyMiddleware.verify_access_token)):
    if(user_info['is_admin'] == True):
        repository = UserStatusRepository(db)
        try:
            data = await repository.add_user_status(user_status_data)
            return data
        except Exception as e:
            return JSONResponse(status_code=404, content={'message':str(e)})
    else:
        return JSONResponse(status_code=403, content={'message':ADMIN_AUTHORIZATION_ERROR})