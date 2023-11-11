from pydantic import BaseModel


class NoCashValuteModel(BaseModel):
    name: str
    code_name: str
    type_valute: str


class CurrentDirection(BaseModel):
    name: str
    partner_link: str
    valute_from: str
    valute_to: str
    in_count: float
    out_count: float
    min_amount: str
    max_amount: str
    # rating: str



# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True
