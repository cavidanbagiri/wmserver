
from pydantic import BaseModel

from datetime import datetime

class GetWarehouseSchema(BaseModel):
    id:int
    document:str
    material_name:str
    quantity:float
    leftover:float
    unit:str
    price:float
    currency:str
    po:str
    certificate:bool
    passport:bool
    created_at:datetime

    project_id:int
    created_by_id:int
    ordered_id:int
    material_code_id:int
    material_type_id:int
    company_id:int

class UpdateWarehouseSchema(BaseModel):
    id:int
    document:str
    material_name:str
    quantity:float
    # leftover:float | None
    unit:str
    price:float
    po:str
    ordered_id:int
    material_type_id:int
    company_id:int

class CreateWarehouseSchema(BaseModel):
    document:str
    material_name:str
    quantity:float
    unit:str
    price:float | None
    currency:str | None
    po:str | None
    certificate:bool=False
    passport:bool=False

    ordered_id:int
    material_code_id:int
    material_type_id:int
    company_id:int


class WarehouseFilterQuerySchema(BaseModel):
    po: str | None = None
    document: str | None = None


class UpdateCertorPassportSchema(BaseModel):
    id: int
    key: str
    value: bool