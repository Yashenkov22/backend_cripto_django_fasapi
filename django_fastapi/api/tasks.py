from celery import shared_task

from .exc import TechServiceWork, NoFoundXmlElement, RobotCheckError
from .services import xml_parser
from .models import Exchange, ExchangeDirection, Direction


#PERIODIC CREATE
@shared_task(name='create_directions_for_exchange')
def create_directions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)

    all_directions = Direction.objects\
                    .select_related('valute_from', 'valute_to')\
                    .values_list('valute_from', 'valute_to').all()
    exchange_directions = exchange.directions\
                    .values_list('valute_from', 'valute_to').all()
    exchange_black_list = exchange.direction_black_list\
                            .values_list('valute_from', 'valute_to').all()
    print('ALL DIRECTION', all_directions)
    print('EXCHANGE DIRECTION', exchange_directions)
    print('BLACK LIST', exchange_black_list)
    direction_list = set(all_directions) - set(exchange_directions) - set(exchange_black_list)
    if direction_list:
        print('RES')
        print(direction_list)
    else:
        print('ПУСТО')

    if direction_list:
        for direction in direction_list:
            valute_from_id, valute_to_id = direction
            dict_for_parse = exchange.__dict__.copy()
            dict_for_parse['valute_from_id'] = valute_from_id
            dict_for_parse['valute_to_id'] = valute_to_id
            if dict_for_parse.get('_state'):
                dict_for_parse.pop('_state')
            create_direction.delay(dict_for_parse)


@shared_task
def create_direction(dict_for_parser: dict):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = xml_parser(dict_for_parser)
    except NoFoundXmlElement:
        not_found_direction = Direction.objects.get(valute_to=dict_for_parser['valute_to_id'],
                                                    valute_from=dict_for_parser['valute_from_id'])
        print('NOT FOUND DIRECTION', not_found_direction)
        Exchange.objects.get(name=dict_for_parser['name'])\
                        .direction_black_list.add(not_found_direction)
    except (TechServiceWork, RobotCheckError) as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('TAKEN WRONG STRUCTURE XML ELEMENT', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parser['name'])
        dict_for_exchange_direction['exchange_name'] = exchange
        ExchangeDirection.objects.create(**dict_for_exchange_direction)        


#PERIODIC UPDATE
@shared_task(name='update_diretions_for_exchange')
def update_diretions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    direction_list = exchange.directions.values_list('valute_from', 'valute_to').all()

    if direction_list:
        for direction in direction_list:
            valute_from_id, valute_to_id = direction
            dict_for_parse = exchange.__dict__.copy()
            dict_for_parse['valute_from_id'] = valute_from_id
            dict_for_parse['valute_to_id'] = valute_to_id
            if dict_for_parse.get('_state'):
                dict_for_parse.pop('_state')
            try_update_direction.delay(dict_for_parse)


@shared_task
def try_update_direction(dict_for_parser: dict):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = xml_parser(dict_for_parser)
    except (TechServiceWork, NoFoundXmlElement, RobotCheckError) as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('TAKEN WRONG STRUCTURE XML ELEMENT', ex)
        pass
    else:
        print('check')
        print(dict_for_exchange_direction)
        
        exchange_direction = ExchangeDirection.objects\
                    .filter(exchange_name=dict_for_parser['name'],
                            valute_from=dict_for_exchange_direction['valute_from'],
                            valute_to=dict_for_exchange_direction['valute_to'],
                            )
        exchange_direction.update(**dict_for_exchange_direction)


#PERIODIC BLACK LIST
@shared_task(name='try_create_directions_from_black_list')
def try_create_directions_from_black_list(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    black_list_directions = exchange.direction_black_list\
                                    .values_list('valute_from', 'valute_to').all()

    if black_list_directions:
        for direction in black_list_directions:
            valute_from_id, valute_to_id = direction
            dict_for_parse = exchange.__dict__.copy()
            dict_for_parse['valute_from_id'] = valute_from_id
            dict_for_parse['valute_to_id'] = valute_to_id
            if dict_for_parse.get('_state'):
                dict_for_parse.pop('_state')
            create_black_list_direction.delay(dict_for_parse)


@shared_task
def create_black_list_direction(dict_for_parser: dict):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = xml_parser(dict_for_parser)
    except (TechServiceWork, NoFoundXmlElement, RobotCheckError) as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('TAKEN WRONG STRUCTURE XML ELEMENT', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parser['name'])
        dict_for_exchange_direction['exchange_name'] = exchange
        ExchangeDirection.objects.create(**dict_for_exchange_direction)

        direction = Direction.objects.get(valute_from=dict_for_exchange_direction['valute_from'],
                                          valute_to=dict_for_exchange_direction['valute_to'])
        exchange.direction_black_list.remove(direction)