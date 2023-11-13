from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Exchange, Direction, ExchangeDirection
from .tasks import try_create_direction



#Signal to add direction for every exchange
@receiver(post_save, sender=Direction)
def add_directions_to_exchanges(sender, instance, created, **kwargs):
    if created:
        exchange_list = Exchange.objects.all()
        for exchange in exchange_list:
            dict_for_parser = exchange.__dict__ | instance.__dict__
            dict_for_parser.pop('_state')

            try_create_direction.delay(dict_for_parser)


#Signal to delete all related direction records
@receiver(post_delete, sender=Direction)
def add_directions_to_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()