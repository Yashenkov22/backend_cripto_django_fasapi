# Generated by Django 4.2.7 on 2023-11-27 02:25

import api.utils.model_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_exchangedirection_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='period_for_update',
            field=models.IntegerField(blank=True, default=60, help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических обновлений', null=True, validators=[api.utils.model_validators.is_positive_validate], verbose_name='Частота обновлений в секундах'),
        ),
    ]
