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
    list_display = ("valute_from", "valute_to", "direction_name")
    # exclude = ['direction_name']
    readonly_fields = ('direction_name', )
    # prepopulated_fields = {
    #     'direction_name': ('valute_from', 'valute_to')
    # }

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        print(form.data)
        obj.direction_name = form.data.get("valute_from") + '->' + form.data.get("valute_to")
        return super().save_model(request, obj, form, change)


@admin.register(ExchangeDirection)
class ExchangeDirectionAdmin(admin.ModelAdmin):
    list_display = ("exchange_name", "valute_from", "valute_to")
