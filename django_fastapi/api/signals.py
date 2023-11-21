from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask

from .models import Exchange, Direction, ExchangeDirection
from .periodic_tasks import (manage_update_periodic_task,
                             periodic_task_for_creation,
                             periodic_task_for_black_list)



#Signal to add direction for every exchange
# @receiver(post_save, sender=Direction)
# def add_directions_to_exchanges(sender, instance, created, **kwargs):
#     if created:
#         exchange_list = Exchange.objects.all()
#         for exchange in exchange_list:
#             dict_for_parser = exchange.__dict__ | instance.__dict__
#             dict_for_parser.pop('_state')

#             try_create_direction.delay(dict_for_parser)


#Signal to delete all related direction records
@receiver(post_delete, sender=Direction)
def delete_directions_to_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()


#Signal to create periodic task for exchange
@receiver(post_save, sender=Exchange)
def create_task_for_exchange(sender, instance, created, **kwargs):
    if created:
        print('PERIODIC TASKS CREATING...')
        periodic_task_for_creation(instance.name)
        manage_update_periodic_task(instance.name, instance.period_for_update)
        periodic_task_for_black_list(instance.name)


#Signal to delete related periodic task for Exchange
@receiver(post_delete, sender=Exchange)
def delete_task_for_exchange(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name__startswith=f'{instance.name}').delete()