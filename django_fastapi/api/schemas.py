from pydantic import BaseModel


class NoCashValuteModel(BaseModel):
    name: str
    code_name: str
    type_valute: str


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True
