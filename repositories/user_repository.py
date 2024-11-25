import asyncio
import os
import uuid
from datetime import datetime, timedelta, timezone

from io import BytesIO

from aiohttp import ClientError
from fastapi import HTTPException

from sqlalchemy import update
from sqlalchemy import select

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Session, joinedload

from db.setup import SessionLocal

# Import Yandex S3
from utils.s3_yandex import s3
import aioboto3
# session = aioboto3.Session(
#                     aws_access_key_id=os.getenv('YANDEX_STORAGE_KEY_ACCESS'),
#                     aws_secret_access_key=os.getenv('YANDEX_STORAGE_SECRET_KEY'),
#                     region_name='ru-central1'
# )

# Import Crypt for hashing password
from passlib.context import CryptContext

# Import Model
from models.user_model import UserModel
from models.user_status_models import UserStatusModel

# Import Schema
from schemas.user_schemas import CreateUserSchema

# Import JWT
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# @@Checked
class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

# @@Checked
class TokenRepository:

    # Create Access Token
    @staticmethod
    def create_access_token( data):
        to_encode = data
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(hours=12) })
        return jwt.encode(to_encode, os.getenv('JWT_SECRET_KEY'), algorithm=os.getenv('JWT_ALGORITHM'))

# @@Checked
class UserLoginRepository(UserRepository):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def login(self, email, password):
        temp_data = await self.db.execute(select(UserModel).options(joinedload(UserModel.user_status).load_only(UserStatusModel.status_code, UserStatusModel.status_name))
                                          .where(UserModel.email == email.lower()))
        data = temp_data.mappings().fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail='User Not found')
        else:
            if self.__verify_password(password, data.password):
                user_data = {
                    "id": data.id,
                    "username": data.first_name.title() + ' ' + data.last_name.title(),
                    "status_code": data.status_code,
                    "status_name": data.status_name.title(),
                    "is_admin": data.is_admin,
                    "project": data.project_id,
                    'profileImage': data.image_url
                }
                token_data = {
                    "id": data.id,
                    "status_code": data.status_code,
                    "is_admin": data.is_admin,
                    "project": data.project_id
                }
                new_data = {}
                new_data['access_token'] = TokenRepository.create_access_token(token_data)
                new_data['user'] = user_data
                return new_data
            else:
                raise HTTPException(status_code=401, detail='Invalid password')

    def __verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)


class UserFetchRepository(UserRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def fetch_users(self):

        # data = self.db.query(UserModel).all()
        data = await self.db.execute(select(UserModel))
        temp = data.mappings().fetchall()
        return temp


class UserProfileImageRepository(UserRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)


    async def upload_image(self, user_info:dict, file)->str:
        async with SessionLocal() as session:
            image_url = await self._upload_file_tostorage(file)
            await session.execute(update(UserModel).where(UserModel.id == user_info['id']).values(
                image_url = image_url
            ))
            await session.commit()
            return image_url


    async def _upload_file_tostorage(self, file):
        if file:
            file_contents = await file.read()
            user_unique_id = uuid.uuid4()
            suffix = file.filename.split('.')[-1]
            file_path = str(user_unique_id)+'.'+suffix
            # s3 = session.client('s3', endpoint_url='https://storage.yandexcloud.net')
            # session = aioboto3.Session(
            #     aws_access_key_id=os.getenv('YANDEX_STORAGE_KEY_ACCESS'),
            #     aws_secret_access_key=os.getenv('YANDEX_STORAGE_SECRET_KEY'),
            #     region_name='ru-central1'
            # )
            s3.upload_fileobj(BytesIO(file_contents), os.getenv('BUCKET_NAME'), 'user_profile_images/'+file_path)
            image_url = f'https://storage.yandexcloud.net/{os.getenv('BUCKET_NAME')}/user_profile_images/{file_path}'
            print('---------------------------- upload image end')
            return image_url


class UserRegisterRepository:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: CreateUserSchema):
        async with SessionLocal() as session:
            try:
                data = UserModel(
                    first_name= user_data.first_name.lower(),
                    last_name= user_data.last_name.lower(),
                    email= user_data.email.lower(),
                    password= self._hash_password(user_data.password),
                    project_id= user_data.project_id,
                    user_status_id = user_data.user_status_id,
                    group_id= user_data.group_id
                )
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data
        
            except IntegrityError as e:
                if 'duplicate key value violates unique constraint ' in str(e):
                    raise HTTPException(status_code=409, detail='User already exists')
                else:
                    raise e
    
    def _hash_password(self, password):
        return self.pwd_context.hash(password)


class UserStatusRepository:

    def __init__(self, db: AsyncSession):
        self.db = db


    async def fetch_user_status(self):
        data = await self.db.execute(select(UserStatusModel))
        temp = data.mappings().all()
        return temp


    async def add_user_status(self, user_status_data):
        async with SessionLocal() as session:
            unique_data = await self._check_unique(user_status_data)
            if unique_data:
                raise HTTPException(status_code=409,
                                    detail=f"{user_status_data} is available. Please Check Again")
            data = UserStatusModel(
                status_name= user_status_data.status_name.lower(),
                status_code= user_status_data.status_code,
            )
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return data

    async def _check_unique(self, user_status_data):
        data = await self.db.execute(select(UserStatusModel).filter(UserStatusModel.status_name == user_status_data.status_name
                                                              or UserStatusModel.status_code == user_status_data.status_code))
        temp = data.first()
        return temp
