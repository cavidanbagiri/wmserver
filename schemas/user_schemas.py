
from pydantic import BaseModel, Field, EmailStr

class GetUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    is_admin: bool = False
    project_id: int
    user_status_id: int
    group_id: int

class CreateUserSchema(BaseModel):
    first_name: str = Field(min_length=2,)
    last_name: str = Field(min_length=2,)
    email: EmailStr
    password: str = Field(min_length=8,)
    project_id: int
    user_status_id: int
    group_id: int

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8,)



class GetUserStatusSchema(BaseModel):
    id: int
    status_name: str
    status_code: str

class CreateUserStatusSchema(BaseModel):
    status_name: str
    status_code: str