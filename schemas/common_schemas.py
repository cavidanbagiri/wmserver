
from pydantic import BaseModel, Field



class GetMaterialCodeSchema(BaseModel):
    id: int
    material_code: str
    material_description: str

class CreateMaterialCodeSchema(BaseModel):
    material_description: str = Field(min_length=3)




class GetProjectSchema(BaseModel):
    id: int
    project_name: str
    project_code: str

class CreateProjectSchema(BaseModel):
    project_name: str = Field(min_length=3)
    project_code: str = Field(min_length=3)




class GetCompanySchema(BaseModel):
    id: int
    company_name:str
    country:str
    email_address:str
    phone_number:str

# This is Checked By Frontend
class CreateCompanySchema(BaseModel):
    company_name: str
    country: str
    email_address: str
    phone_number: str




class GetGroupSchema(BaseModel):
    id: int
    group_name: str

class CreateGroupSchema(BaseModel):
    group_name: str




class GetOrderedSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    project_id: int
    group_id: int
    username: str
    project: GetProjectSchema
    group: GetGroupSchema

class CreateOrderedSchema(BaseModel):
    first_name: str
    last_name: str
    project_id: int
    group_id: int



class GetMaterialTypeSchema(BaseModel):
    id: int
    name: str


class CreateMaterialTypeSchema(BaseModel):
    name: str
