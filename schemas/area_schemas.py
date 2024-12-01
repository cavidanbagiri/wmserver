
from pydantic import BaseModel

class CreateAreaSchema(BaseModel):

    quantity:float
    serial_number:str
    material_id:str
    provide_type:str
    card_number:str
    username:str

    stock_id:int
    group_id:int
