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
    list_display = ("valute_from", "valute_to")


@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("exchange_name", "valute_from", "valute_to")
