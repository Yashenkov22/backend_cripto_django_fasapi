from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest

from api.models import Exchange, Direction, ExchangeDirection, NoCashValute
from api.periodic_tasks import manage_periodic_task


class DirectionTabular(admin.StackedInline):
    model=ExchangeDirection
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "xml_url", "partner_link")
    inlines = [DirectionTabular]

    def save_model(self, request, obj, form, change):
        update_fields = []

        # True if something changed in model
        # Note that change is False at the very first time
        if change: 

            for key, value in form.cleaned_data.items():
                # True if something changed in model
                # print(obj.name)
                # print('key', key)
                # print('value', value)
                if value != form.initial[key]:
                    if key == 'period_for_update':
                        manage_periodic_task(obj.name, value)
                        # print('PERIOD', form.initial[key])
                    update_fields.append(key)

            obj.save(update_fields=update_fields)
        else:
            print('NOT CHANGE!!!!')
            return super().save_model(request, obj, form, change)


@admin.register(NoCashValute)
class NoCashValuteAdmin(admin.ModelAdmin):
    list_display = ("name", "code_name", "type_valute")


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("get_direction_name", )

    def has_change_permission(self, request, obj = None):
        return False

    def get_direction_name(self, obj):
        return f'{obj.valute_from} -> {obj.valute_to}'


@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("get_display_name", )

    def has_change_permission(self, request, obj = None):
        return False
    
    def has_add_permission(self, request, obj = None):
        return False

    def get_display_name(self, obj):
        return f'{obj.exchange_name} ({obj.valute_from} -> {obj.valute_to})'
