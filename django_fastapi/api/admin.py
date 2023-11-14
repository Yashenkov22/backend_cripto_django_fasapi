from typing import Any
from django.contrib import admin

from api.models import Exchange, Direction, ExchangeDirection, NoCashValute


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ("name", "xml_url", "partner_link")


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
