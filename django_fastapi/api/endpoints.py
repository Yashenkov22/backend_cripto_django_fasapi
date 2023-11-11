from typing import List

from fastapi import APIRouter

from api import models, schemas


api_router = APIRouter()


# @api_router.post("/items", response_model=schemas.Item)
# def create_item(item: schemas.ItemCreate):
#     item = models.Item.objects.create(**item.dict())

#     return item


@api_router.get("/valute/no_cash", response_model=List[schemas.NoCashValuteModel])
def read_items():
    # items = models.NoCashValute.objects.all()
    exchange_list = models.Exchange.objects.all()
    for exchange in exchange_list:
        print(exchange.__dict__)
    return exchange_list
