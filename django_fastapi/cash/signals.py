from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask

from .models import Exchange, Direction, ExchangeDirection
from .periodic_tasks import (manage_periodic_task_for_update,
                             periodic_task_for_creation,
                             periodic_task_for_black_list)


#Signal to delete all related direction records
@receiver(post_delete, sender=Direction)
def delete_directions_from_exchanges(sender, instance, **kwargs):
    direction_list = ExchangeDirection.objects.filter(valute_from=instance.valute_from,
                                                      valute_to=instance.valute_to).all()
    direction_list.delete()


#Signal to create periodic task for exchange
@receiver(post_save, sender=Exchange)
def create_tasks_for_exchange(sender, instance, created, **kwargs):
    if created:
        print('CASH PERIODIC TASKS CREATING...')
        periodic_task_for_creation(instance.name)
        manage_periodic_task_for_update(instance.name, instance.period_for_update)
        periodic_task_for_black_list(instance.name)


#Signal to delete related periodic task for Exchange
@receiver(post_delete, sender=Exchange)
def delete_task_for_exchange(sender, instance, **kwargs):
    PeriodicTask.objects.filter(name__startswith=f'{instance.name} cash').delete()