from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from no_cash.models import Exchange, Direction, ExchangeDirection
from no_cash.periodic_tasks import manage_periodic_task_for_update


class ExchangeDirectionTabular(admin.StackedInline):
    model=ExchangeDirection
    # readonly_fields = ('is_active', )
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "xml_url", 'is_active')
    readonly_fields = ('direction_black_list', 'is_active')
    inlines = [ExchangeDirectionTabular]

    def save_model(self, request, obj, form, change):
        update_fields = []

        if change: 
            for key, value in form.cleaned_data.items():
                # print(obj.name)
                # print('key', key)
                # print('value', value)
                if value != form.initial[key]:
                    if key == 'period_for_update':
                        manage_periodic_task_for_update(obj.name, value)
                        # print('PERIOD', form.initial[key])
                    update_fields.append(key)

            obj.save(update_fields=update_fields)
        else:
            print('NOT CHANGE!!!!')
            return super().save_model(request, obj, form, change)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("get_direction_name", )
    ordering = ('valute_from', 'valute_to')

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
        return f'{obj.exchange} ({obj.valute_from} -> {obj.valute_to})'
