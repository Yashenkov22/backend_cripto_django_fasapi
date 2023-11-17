import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def get_or_create_schedule(period: int):
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=period,
                            period=IntervalSchedule.SECONDS
                        )
    return schedule


def manage_periodic_task(exchange_name: str, period: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} task')
    except PeriodicTask.DoesNotExist:
        if not period:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule(period)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} task',
                    task='update_diretions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if not period:
            task.delete()
        else:
            schedule = get_or_create_schedule(period)
            task.interval = schedule
            task.save()