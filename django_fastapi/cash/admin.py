from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from .periodic_tasks import manage_periodic_task_for_update

from .models import Country, City, Exchange, Direction, ExchangeDirection


class CityStacked(admin.StackedInline):
    model = City
    extra = 0
    fields = ('is_parse', )
    ordering = ('-is_parse', 'name')
    

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    inlines = [CityStacked]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'country', 'is_parse')
    list_editable = ('is_parse', )
    list_select_related = ('country', )
    ordering = ('-is_parse', 'name')
    search_fields = ('name', 'country__name')
    list_per_page = 20


class ExchangeDirectionTabular(admin.StackedInline):
    model = ExchangeDirection
    ordering = ('city', 'valute_from', 'valute_to')
    
    def has_change_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False
    
    def has_add_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        return False


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", 'is_active')
    readonly_fields = ('is_active', 'direction_black_list')
    inlines =[ExchangeDirectionTabular]

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
    list_display = ('get_direction_name', )
    list_select_related = ('valute_from', 'valute_to')

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
        return f'{obj.exchange} ({obj.city}: {obj.valute_from} -> {obj.valute_to})'