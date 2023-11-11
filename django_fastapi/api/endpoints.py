from typing import List

from fastapi import APIRouter

from api import models, schemas


api_router = APIRouter()

#rating ?
@api_router.get("/directions", response_model=List[schemas.CurrentDirection])
def get_current_direction_list(valute_from: str, valute_to: str):
    queries = models.ExchangeDirection.objects\
            .filter(valute_from=valute_from,valute_to=valute_to)\
            .select_related('exchange_name').all()
    direction_list = []
    for query in queries:
        direction = query.__dict__ | query.exchange_name.__dict__
        direction_list.append(direction)
    return direction_list
    
    


@api_router.get("/valute/no_cash", response_model=List[schemas.NoCashValuteModel])
def get_valute_list():
    # items = models.NoCashValute.objects.all()
    return models.NoCashValute.objects.all()
