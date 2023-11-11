from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Exchange, Direction, ExchangeDirection
from .services import xml_parser
from .exc import TechServiceWork, NoFoundXmlElement, RobotCheckError



#Signal to add direction for every exchange
@receiver(post_save, sender=Direction)
def add_directions_to_exchanges(sender, instance, created, **kwargs):
    if created:
        exchange_list = Exchange.objects.all()
        for exchange in exchange_list:
            dict_for_parser = exchange.__dict__ | instance.__dict__
            # print(dict_for_parser)
            try:
                dict_for_exchange_direction = xml_parser(dict_for_parser)
            except (TechServiceWork, NoFoundXmlElement, RobotCheckError):
                continue
            else:
                dict_for_exchange_direction['exchange_name'] = exchange
                ExchangeDirection.objects.create(**dict_for_exchange_direction)


@receiver(post_delete, sender=Direction)
def add_directions_to_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()