import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def create_periodic_task(exchange_name: str, period: int):
    schedule, created = IntervalSchedule.objects.get_or_create(
                            every=period,
                            period=IntervalSchedule.SECONDS
                        )
    PeriodicTask.objects.create(
            interval=schedule,
            name=f'{exchange_name} task',
            task='update_diretions_for_exchange',
            args=json.dumps([exchange_name,])
            )


def manage_periodic_task(exchange_name: str, period: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} task')
    except PeriodicTask.DoesNotExist:
        if period == 0:
            print('PASS')
            pass
        else:
            create_periodic_task(exchange_name, period)
    else:
        task.delete()

        if period == 0:
            pass
        else:
            create_periodic_task(exchange_name, period)
