import re
import requests

from xml.etree import ElementTree as ET

from django_celery_beat.models import IntervalSchedule

from general_models.models import BaseExchange
from .exc import RobotCheckError


def get_or_create_schedule(interval: int, period: str):
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=interval,
                            period=period,
                        )
    return schedule
   

def check_exchange_and_try_get_xml_file(exchange: BaseExchange):
    try:
        is_active, xml_file = check_for_active_and_try_get_xml(exchange.xml_url)
    except Exception as ex:
        print('CHECK ACTIVE EXCEPTION!!!', ex)
        return None
    else:
        if exchange.is_active != is_active:
            exchange.is_active = is_active
            print('CHANGE IS_ACTIVE')
            exchange.save()
        
        return xml_file
    

def check_for_active_and_try_get_xml(xml_url: str):
    resp = requests.get(xml_url)
    headers = resp.headers

    if not re.match(r'^[a-zA-Z]+\/xml?', headers['Content-Type']):
        raise RobotCheckError(f'{xml_url} требует проверку на робота')
    else:
        xml_file = resp.text
        print(xml_url)
        root = ET.fromstring(xml_file)
        is_active = True
        if root.text == 'Техническое обслуживание':
            is_active = False
        return (is_active, xml_file)