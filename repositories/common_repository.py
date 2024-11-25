import time
import asyncio
from abc import ABC, abstractmethod
from typing import Union

from fastapi import HTTPException

# Import Session Local for add, commit, query data
from db.setup import SessionLocal

# Import Sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.sql import text
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession


# Import Models
from models.material_code_model import MaterialCodeModel
from models.material_type_model import MaterialTypeModel
from models.project_model import ProjectModel
from models.company_model import CompanyModel
from models.group_model import GroupModel
from models.ordered_model import OrderedModel

class CommonAbstractClass(ABC):

    @abstractmethod
    async def fetch(self):
        pass

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass

# Import Schemas
from schemas.common_schemas import *

# Tested
class MaterialCodeRepository (CommonAbstractClass):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch(self):
        data = await self.db.execute(select(MaterialCodeModel))
        temp = data.mappings().all()
        return temp

    async def filter(self, value: Union[str, None]=None):
        data = await self.db.execute(select(MaterialCodeModel).filter(MaterialCodeModel.material_description.ilike(f'%{value}%')))
        temp = data.mappings().all()
        return temp

    async def get_byid(self, id: int):
        data = await self.db.execute(select(MaterialCodeModel).filter(MaterialCodeModel.id == id))
        temp = data.first()
        return temp
    
    async def create(self, material_code_data: CreateMaterialCodeSchema):

        async with SessionLocal() as session:
            data = await self._check_unique(material_code_data.material_description)
            if data:
                raise HTTPException(status_code=409, detail=f'{material_code_data.material_description.title()} is available. Please check again')
            query = 'select id from material_codes order by id desc limit 1'
            result = await self.db.execute(text(query))
            id = 0
            data = result.first()
            if result is not None and data is not None:
                id = data[0]
                material_code = id + 1 + 1000000
            else:
                id = 1000000
                material_code = id + 1
            result.close()
            data = MaterialCodeModel(
                material_code = str(material_code),
                material_description = material_code_data.material_description.lower()
                )
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return data

    async def _check_unique(self, material_description: str):
        data = await self.db.execute(select(MaterialCodeModel).filter(MaterialCodeModel.material_description == material_description.lower()))
        temp = data.first()
        return temp


# Checked For Async Await
class ProjectRepository (CommonAbstractClass):

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def fetch(self):
        data = await self.db.execute(select(ProjectModel))
        temp = data.mappings().all()
        return temp
    
    async def create(self, project_data: CreateProjectSchema):
        async with SessionLocal() as session:
            unique = await self._check_unique(project_data.project_name)
            if unique:
                raise HTTPException(status_code=409, detail=f'{project_data.project_name} is available. Please check again')
            else:
                data = ProjectModel(project_name= project_data.project_name.upper(), project_code= project_data.project_code)
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data

    async def _check_unique(self, project_name):
        data = await self.db.execute(select(ProjectModel).filter(ProjectModel.project_name == project_name.upper()))
        temp = data.first()
        return temp


# Checked For Async Await
class CompanyRepository (CommonAbstractClass):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch(self):
        data = await self.db.execute(select(CompanyModel))
        temp = data.mappings().all()
        return temp

    async def filter(self, company_name: Union[str, None] = None):
        data = await self.db.execute(select(CompanyModel).filter(CompanyModel.company_name.ilike(f'%{company_name}%')))
        temp = data.mappings().all()
        return temp

    async def create(self, company_data: CreateCompanySchema):
        async with SessionLocal() as session:
            unique = await self._check_unique(company_data.company_name)
            if unique:
                raise HTTPException(status_code=409, detail=f'{company_data.company_name} is available. Please check again')
            data = CompanyModel(
                company_name = company_data.company_name,
                country = company_data.country,
                email_address = company_data.email_address,
                phone_number = company_data.phone_number
            )
            session.add(data)
            await session.commit()
            await session.refresh(data)
            return data

    async def _check_unique(self, company_name):
        data = await self.db.execute(select(CompanyModel).filter(func.lower(CompanyModel.company_name) == func.lower(company_name)))
        temp = data.first()
        return temp


# Checked For Async Await
class GroupRepository (CommonAbstractClass):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch(self):
        data = await self.db.execute(select(GroupModel))
        temp = data.mappings().all()
        return temp

    async def create(self, group_data: CreateGroupSchema):

        async with SessionLocal() as session:

            data = await self._check_unique(group_data.group_name)
            if data:
                raise HTTPException(status_code=409, detail=f"{group_data.group_name.title()} is available. Please Check Again")
            else:
                data = GroupModel(
                    group_name = group_data.group_name.lower(),
                )
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data

    async def _check_unique(self, group_name):
        data = await self.db.execute(select(GroupModel).filter(GroupModel.group_name == group_name.lower()))
        second = data.first()
        return second


# Checked For Async Await
class OrderedRepository (CommonAbstractClass):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch(self):
        data = await self.db.execute(select(OrderedModel, func.upper(func.concat(OrderedModel.first_name, ' ', OrderedModel.last_name)).label('username')
                       ).options(selectinload(OrderedModel.group)).options(
            selectinload(OrderedModel.project)))
        temp = data.mappings().all()
        return temp


    async def filter(self, ordered: Union[str, None] = None):
        data = await self.db.execute(select(OrderedModel, func.upper(func.concat(OrderedModel.first_name, ' ', OrderedModel.last_name)).label('username')).filter(OrderedModel.first_name.ilike(f'%{ordered}%')))
        temp = data.mappings().all()
        return temp

    async def create(self, ordered_data: CreateOrderedSchema):
        async with SessionLocal() as session:
            check_data = await self._check_unique(ordered_data)
            if check_data:
                raise HTTPException(status_code=409, detail=f"{ordered_data.first_name.title()} {ordered_data.last_name.title()} is already available")
            else:
                data = OrderedModel(
                    first_name = ordered_data.first_name.lower(),
                    last_name = ordered_data.last_name.lower(),
                    project_id = ordered_data.project_id,
                    group_id = ordered_data.group_id
                )
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data

    async def _check_unique(self, ordered_data: CreateOrderedSchema):
        data = await self.db.execute(select(OrderedModel).filter(OrderedModel.first_name == ordered_data.first_name.lower() and OrderedModel.last_name == ordered_data))
        temp = data.first()
        return temp


class MaterialTypeRepository (CommonAbstractClass):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch(self):
        data = await self.db.execute(select(MaterialTypeModel))
        temp = data.mappings().all()
        return temp

    async def create(self, material_type_data: CreateMaterialTypeSchema):
        async with SessionLocal() as session:
            check_data = await self._check_unique(material_type_data)
            if check_data:
                raise HTTPException(status_code=409, detail=f"{material_type_data.name.title()} is already available")
            else:
                data = MaterialTypeModel(
                    name = material_type_data.name.lower()
                )
                session.add(data)
                await session.commit()
                await session.refresh(data)
                return data

    async def _check_unique(self, material_type_data: CreateMaterialTypeSchema):
        data = await self.db.execute(select(MaterialTypeModel).filter(MaterialTypeModel.name == material_type_data.name.lower()))
        temp = data.first()
        return temp