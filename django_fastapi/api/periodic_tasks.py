import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .utils.periodic_tasks import get_or_create_schedule


# def get_or_create_schedule_for_update(interval: int):
#     schedule, _ = IntervalSchedule.objects.get_or_create(
#                             every=interval,
#                             period=IntervalSchedule.SECONDS
#                         )
#     return schedule


def manage_periodic_task_for_update(exchange_name: str, interval: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} task update')
    except PeriodicTask.DoesNotExist:
        if interval == 0:
            print('PASS')
            pass
        else:
            # schedule = get_or_create_schedule_for_update(interval)
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} task update',
                    task='update_diretions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        #?
        # exchange_tasks = PeriodicTask.objects.filter(name__startswith=f'{exchange_name}')
        # for task in exchange_tasks:
        #      task.enabled = False
        if interval == 0:
            task.enabled = False
        else:
            task.enabled = True
            # schedule = get_or_create_schedule_for_update(interval)
            schedule = get_or_create_schedule(interval, IntervalSchedule.SECONDS)
            task.interval = schedule
        task.save()


def periodic_task_for_creation(exchange_name: str):
        # schedule, _ = IntervalSchedule.objects.get_or_create(
        #                     every=90,
        #                     period=IntervalSchedule.SECONDS
        #                 )
        schedule = get_or_create_schedule(90, IntervalSchedule.SECONDS)
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'{exchange_name} task creation',
            task='create_directions_for_exchange',
            args=json.dumps([exchange_name,]),
        )


def periodic_task_for_black_list(exchange_name: str):
        # schedule, _ = IntervalSchedule.objects.get_or_create(
        #                     every=1,
        #                     period=IntervalSchedule.DAYS
        #                 )
        schedule = get_or_create_schedule(1, IntervalSchedule.DAYS)
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'{exchange_name} task black list',
            task='try_create_directions_from_black_list',
            args=json.dumps([exchange_name,]),
        )