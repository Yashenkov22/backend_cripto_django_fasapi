import requests

from xml.etree import ElementTree as ET

from django_celery_beat.models import IntervalSchedule
from api.models import Exchange
from api.exc import RobotCheckError, TechServiceWork
from celery.local import Proxy


def get_or_create_schedule(interval: int, period: str):
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=interval,
                            period=period,
                        )
    return schedule


# def run_background_tasks(task: Proxy, exchange: Exchange, direction_list: set):
#     for direction in direction_list:
#         valute_from_id, valute_to_id = direction
#         dict_for_parse = exchange.__dict__.copy()
#         dict_for_parse['valute_from_id'] = valute_from_id
#         dict_for_parse['valute_to_id'] = valute_to_id
#         if dict_for_parse.get('_state'):
#             dict_for_parse.pop('_state')
#         task.delay(dict_for_parse)

def run_background_tasks(task: Proxy,
                         exchange: Exchange,
                         direction_list: set,
                         xml_file: str):
    for direction in direction_list:
        valute_from_id, valute_to_id = direction
        dict_for_parse = exchange.__dict__.copy()
        dict_for_parse['valute_from_id'] = valute_from_id
        dict_for_parse['valute_to_id'] = valute_to_id
        if dict_for_parse.get('_state'):
            dict_for_parse.pop('_state')
        task.delay(dict_for_parse, xml_file)



def check_for_tech_work(xml_url: str):
    resp = requests.get(xml_url)
    headers = resp.headers

    if headers['Content-Type'] != 'text/xml; charset=UTF-8':
        raise RobotCheckError(f'{xml_url} требует проверку на робота')
    else:
        xml_file = resp.text
        print(xml_url)
        root = ET.fromstring(xml_file)
        error_text = root.text
        is_active_status = True
        if error_text == 'Техническое обслуживание':
            # raise TechServiceWork(f'Техническое обслуживание по адресу {xml_url}')
            # return (False, xml_file)
            is_active_status = False
        return (is_active_status, xml_file)
    

def check_exchange_and_try_get_data(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    try:
        is_active, xml_file = check_for_tech_work(exchange.xml_url)
    except RobotCheckError as ex:
        print('CATCH EXCEPTION', ex)
        return None
    except Exception as ex:
        print('EXCEPTION!!!', ex)
        return None
    else:
        if exchange.is_active != is_active:
            exchange.is_active = is_active
            print('CHANGE IS_ACTIVE')
            exchange.save()
        
        return (
            exchange,
            is_active,
            xml_file,
        )