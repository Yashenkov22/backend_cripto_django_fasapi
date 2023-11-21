import json

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def get_or_create_schedule_for_update(period: int):
    schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=period,
                            period=IntervalSchedule.SECONDS
                        )
    return schedule


def manage_update_periodic_task(exchange_name: str, period: int):
    try:
        task = PeriodicTask.objects.get(name=f'{exchange_name} task update')
    except PeriodicTask.DoesNotExist:
        if not period:
            print('PASS')
            pass
        else:
            schedule = get_or_create_schedule_for_update(period)
            PeriodicTask.objects.create(
                    interval=schedule,
                    name=f'{exchange_name} task update',
                    task='update_diretions_for_exchange',
                    args=json.dumps([exchange_name,]),
                    )
    else:
        if not period:
            task.delete()
        else:
            schedule = get_or_create_schedule_for_update(period)
            task.interval = schedule
            task.save()


def periodic_task_for_creation(exchange_name: str):
        schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=60,
                            period=IntervalSchedule.SECONDS
                        )
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'{exchange_name} task creation',
            task='create_directions_for_exchange',
            args=json.dumps([exchange_name,]),
        )


def periodic_task_for_black_list(exchange_name: str):
        schedule, _ = IntervalSchedule.objects.get_or_create(
                            every=300,
                            period=IntervalSchedule.SECONDS
                        )
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'{exchange_name} task black list',
            task='try_create_directions_from_black_list',
            args=json.dumps([exchange_name,]),
        )