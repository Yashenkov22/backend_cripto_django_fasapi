from django.db.models.signals import post_save, post_delete, pre_save
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
def delete_directions_to_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()



#Signal to delete all related direction records
# @receiver(pre_save, sender=Exchange)
# def add_direct(sender, instance, **kwargs):
#         print(instance.__dict__)
#         print('BEFORE UPDATED!!!!', kwargs)


# @receiver(post_save, sender=Exchange)
# def add_direct(sender, instance, created, **kwargs):
#         print(instance.__dict__)
#         print('AFTER UPDATED!!!!', kwargs)
    

