# Generated by Django 4.2.7 on 2023-11-23 02:56

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_exchange_period_for_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direction',
            options={'ordering': ['valute_from', 'valute_to'], 'verbose_name': 'Направление для обмена', 'verbose_name_plural': 'Направления для обмена'},
        ),
        migrations.AlterField(
            model_name='exchange',
            name='direction_black_list',
            field=models.ManyToManyField(to='api.direction', verbose_name='Чёрный список'),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='period_for_update',
            field=models.IntegerField(blank=True, default=60, help_text='Значение - положительное целое число, при установлении в 0, останавливает задачу переодических обновлений', null=True, validators=[api.models.is_positive_validate], verbose_name='Частота обновлений в секундах'),
        ),
    ]