from django.contrib import admin

from django_celery_beat.models import (SolarSchedule,
                                       PeriodicTask,
                                       IntervalSchedule,
                                       ClockedSchedule,
                                       CrontabSchedule)

from .models import Valute


#DONT SHOW PERIODIC TASKS IN ADMIN PANEL
admin.site.unregister(SolarSchedule)
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(CrontabSchedule)


@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'type_valute')
