import re
import requests

from xml.etree import ElementTree as ET

from django_celery_beat.models import IntervalSchedule
from no_cash.models import Exchange
from no_cash.exc import RobotCheckError
from celery.local import Proxy


def get_or_create_schedule(interval: int, period: str):
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=interval,
                            period=period,
                        )
    return schedule


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
   

def check_exchange_and_try_get_data_for_parse(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)
    try:
        is_active, xml_file = check_for_active_and_try_get_xml(exchange.xml_url)
    # except RobotCheckError as ex:
    #     print('CATCH EXCEPTION', ex)
    #     return None
    except Exception as ex:
        print('CHECK ACTIVE EXCEPTION!!!', ex)
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
    
    
def check_for_active_and_try_get_xml(xml_url: str):
    resp = requests.get(xml_url)
    headers = resp.headers

    # if headers['Content-Type'] != 'text/xml; charset=UTF-8':
    if not re.match(r'^[a-zA-Z]+\/xml?', headers['Content-Type']):
        raise RobotCheckError(f'{xml_url} требует проверку на робота')
    else:
        xml_file = resp.text
        print(xml_url)
        root = ET.fromstring(xml_file)
        # error_text = root.text
        is_active = True
        if root.text == 'Техническое обслуживание':
            is_active = False
        return (is_active, xml_file)