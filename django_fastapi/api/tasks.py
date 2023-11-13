from celery import shared_task

from .exc import TechServiceWork, NoFoundXmlElement, RobotCheckError
from .services import xml_parser
from .models import Exchange, ExchangeDirection


@shared_task
def try_create_direction(dict_for_parser: dict):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = xml_parser(dict_for_parser)
    except (TechServiceWork, NoFoundXmlElement, RobotCheckError):
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parser['name'])
        dict_for_exchange_direction['exchange_name'] = exchange
        ExchangeDirection.objects.create(**dict_for_exchange_direction)