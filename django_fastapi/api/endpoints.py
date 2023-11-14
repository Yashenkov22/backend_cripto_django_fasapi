from typing import List
from collections import defaultdict

from fastapi import APIRouter

from . import models, schemas


api_router = APIRouter()

#rating ?
@api_router.get("/directions", response_model=List[schemas.CurrentDirection])
def get_current_direction_list(valute_from: str, valute_to: str):
    queries = models.ExchangeDirection.objects\
            .filter(valute_from=valute_from,valute_to=valute_to)\
            .select_related('exchange_name').all()
    direction_list = []

    for query in queries:
        if query.exchange_name.__dict__.get('partner_link'):
            query.exchange_name.__dict__['partner_link'] += f'?cur_from={valute_from}&cur_to={valute_to}'
        direction = query.__dict__ | query.exchange_name.__dict__
        direction_list.append(direction)

    return direction_list
    

@api_router.get("/valute/no_cash")
def get_valute_list():
    list_valute = models.NoCashValute.objects.all()

    list_type_valute = list_valute.values_list('type_valute').distinct('type_valute')
    default_dict_keys = tuple(map(lambda el: el[0], list_type_valute))

    json_dict = defaultdict(list)
    json_dict.fromkeys(default_dict_keys)

    for valute in list_valute:
        json_dict[valute.type_valute].append(schemas.NoCashValuteModel(**valute.__dict__))

    return json_dict
