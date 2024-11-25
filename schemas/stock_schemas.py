

from pydantic import BaseModel

class FetchStockSchema(BaseModel):
    id:int
    quantity:float
    stock:float | None = None
    serial_number:str
    material_id:str
    created_by_id:int
    warehouse_id:int



class CreateStockSchema(BaseModel):
    id: int
    quantity:float
    leftover:float
    entered_amount: float
    serial_number:str
    material_id:str
    created_by_id:int
    warehouse_id:int
