from celery import shared_task

from django.core.cache import cache

from .exc import NoFoundXmlElement
from .utils.parsers import parse_xml
from .utils.periodic_tasks import (run_background_tasks,
                                   check_exchange_and_try_get_data_for_parse)
from .models import Exchange, ExchangeDirection, Direction


#PERIODIC CREATE
@shared_task(name='create_directions_for_exchange')
def create_directions_for_exchange(exchange_name: str):
    data_for_parse = check_exchange_and_try_get_data_for_parse(exchange_name)
    if data_for_parse is not None:
        exchange, is_active, xml_file = data_for_parse
        if is_active:
            #CACHE
            all_directions = cache.get('all_directions')
            if not all_directions:
                all_directions = Direction.objects\
                                        .select_related('valute_from', 'valute_to')\
                                        .values_list('valute_from', 'valute_to').all()
                cache.set('all_directions', all_directions, 60)
                print('SET VALUE TO CACHE')
            else:
                print('VALUE GETTING FROM CACHE')
                
            exchange_directions = exchange.directions\
                                        .values_list('valute_from', 'valute_to').all()
            exchange_black_list_directions = exchange.direction_black_list\
                                        .values_list('valute_from', 'valute_to').all()
            print('ALL DIRECTION', all_directions)
            print('EXCHANGE DIRECTION', exchange_directions)
            print('BLACK LIST', exchange_black_list_directions)
            direction_list = set(all_directions) - set(exchange_directions) - set(exchange_black_list_directions)

            if direction_list:
                run_background_tasks(create_direction,
                                     exchange,
                                     direction_list,
                                     xml_file)


@shared_task
def create_direction(dict_for_parse: dict,
                     xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_create_exchange_direction = parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement:
        not_found_direction = Direction.objects.get(valute_to=dict_for_parse['valute_to_id'],
                                                    valute_from=dict_for_parse['valute_from_id'])
        print('NOT FOUND DIRECTION', not_found_direction)
        Exchange.objects.get(name=dict_for_parse['name'])\
                        .direction_black_list.add(not_found_direction)
    except Exception as ex:
        print('PARSE FAILED', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parse['name'])
        dict_for_create_exchange_direction['exchange'] = exchange
        ExchangeDirection.objects.create(**dict_for_create_exchange_direction)


#PERIODIC UPDATE
@shared_task(name='update_diretions_for_exchange')
def update_diretions_for_exchange(exchange_name: str):
    data_for_parse = check_exchange_and_try_get_data_for_parse(exchange_name)
    if data_for_parse is not None:
        exchange, is_active, xml_file = data_for_parse
        if is_active:
            direction_list = exchange.directions.values_list('valute_from', 'valute_to').all()

            if direction_list:
                run_background_tasks(try_update_direction,
                                     exchange,
                                     direction_list,
                                     xml_file)


@shared_task
def try_update_direction(dict_for_parse: dict,
                         xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_update_exchange_direction = parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('PARSE UPDATE FAILED', ex)
        pass
    else:
        print('update')
        # print(dict_for_update_exchange_direction)
        
        exchange_direction = ExchangeDirection.objects\
                            .filter(exchange=dict_for_parse['name'],
                            valute_from=dict_for_update_exchange_direction['valute_from'],
                            valute_to=dict_for_update_exchange_direction['valute_to'],
                            )
        exchange_direction.update(**dict_for_update_exchange_direction)


#PERIODIC BLACK LIST
@shared_task(name='try_create_directions_from_black_list')
def try_create_directions_from_black_list(exchange_name: str):
    data_for_parse = check_exchange_and_try_get_data_for_parse(exchange_name)
    if data_for_parse is not None:
        exchange, is_active, xml_file = data_for_parse
        if is_active:
            black_list_directions = exchange.direction_black_list\
                                            .values_list('valute_from', 'valute_to').all()

            if black_list_directions:
                run_background_tasks(try_create_black_list_direction,
                                     exchange,
                                     black_list_directions,
                                     xml_file)


@shared_task
def try_create_black_list_direction(dict_for_parse: dict,
                                    xml_file: str):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = parse_xml(dict_for_parse, xml_file)
    except NoFoundXmlElement as ex:
        print('CATCH EXCEPTION', ex)
        pass
    except Exception as ex:
        print('BLACK LIST PARSE FAILED', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parse['name'])
        dict_for_exchange_direction['exchange'] = exchange
        ExchangeDirection.objects.create(**dict_for_exchange_direction)

        direction = Direction.objects.get(valute_from=dict_for_exchange_direction['valute_from'],
                                          valute_to=dict_for_exchange_direction['valute_to'])
        exchange.direction_black_list.remove(direction)