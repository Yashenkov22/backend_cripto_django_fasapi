from celery import shared_task

from .exc import TechServiceWork, NoFoundXmlElement, RobotCheckError
from .services import xml_parser
from .models import Exchange, ExchangeDirection, Direction


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
        # print('check')
        # print(dict_for_exchange_direction)
        ExchangeDirection.objects.create(**dict_for_exchange_direction)        


@shared_task
def try_update_direction(dict_for_parser: dict):
    print('*' * 10)
    print('inside task')

    try:
        dict_for_exchange_direction = xml_parser(dict_for_parser)
    except (TechServiceWork, NoFoundXmlElement, RobotCheckError) as ex:
        print('CATCH EXCEPTION', ex)
        pass
    else:
        exchange = Exchange.objects.get(name=dict_for_parser['name'])
        dict_for_exchange_direction['exchange_name'] = exchange
        print('check')
        print(dict_for_exchange_direction)
        
        direction = ExchangeDirection.objects\
                    .filter(exchange_name=dict_for_parser['name'],
                            valute_from=dict_for_exchange_direction['valute_from'],
                            valute_to=dict_for_exchange_direction['valute_to'],
                            )
        if not direction:
            ExchangeDirection.objects.create(**dict_for_exchange_direction)
        else:
            direction.update(**dict_for_exchange_direction)


@shared_task(name='update_diretions_for_exchange')
def update_diretions_for_exchange(exchange_name: str):
    exchange = Exchange.objects.get(name=exchange_name)

    direction_list = Direction.objects.select_related('valute_from', 'valute_to').all()

    if direction_list:
        for direct in direction_list:
            # print(direct.__dict__)
            dict_for_parse = exchange.__dict__ | direct.__dict__
            dict_for_parse.pop('_state')
            try_update_direction.delay(dict_for_parse)
            # print(dict_for_parse)
        # print('INSIDE TASK!!!!')
