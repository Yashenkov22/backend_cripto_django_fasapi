from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.conf import settings

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

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'get_icon', 'type_valute')
    fields = ('name', 'code_name', 'icon_url', 'get_icon', 'type_valute')
    readonly_fields = ('get_icon', )
    search_fields = ('name', )

    def get_icon(self, obj):
        if obj.icon_url:
            return mark_safe(f"<img src='http://{settings.SITE_DOMAIN}{settings.DJANGO_PREFIX}{obj.icon_url.url}' width=40")
        
    get_icon.short_description = 'Текущая иконка'