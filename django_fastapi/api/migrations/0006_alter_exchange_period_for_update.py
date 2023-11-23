# Generated by Django 4.2.7 on 2023-11-20 07:53

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_exchange_direction_black_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='period_for_update',
            field=models.IntegerField(blank=True, default=120, null=True, validators=[api.models.is_positive_validate], verbose_name='Частота обновлений в секундах'),
        ),
    ]