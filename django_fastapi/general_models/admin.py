from django.contrib import admin

from .models import Valute

@admin.register(Valute)
class ValuteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code_name', 'type_valute')
