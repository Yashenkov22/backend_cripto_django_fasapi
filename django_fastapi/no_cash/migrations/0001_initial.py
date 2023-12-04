# Generated by Django 4.2.7 on 2023-12-04 04:30

from django.db import migrations, models
import django.db.models.deletion
import general_models.utils.model_validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.ForeignKey(limit_choices_to=models.Q(('type_valute', 'Наличные'), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='no_cash_valutes_from', to='general_models.valute', to_field='code_name', verbose_name='Отдаём')),
                ('valute_to', models.ForeignKey(limit_choices_to=models.Q(('type_valute', 'Наличные'), _negated=True), on_delete=django.db.models.deletion.CASCADE, related_name='no_cash_valutes_to', to='general_models.valute', to_field='code_name', verbose_name='Получаем')),
            ],
            options={
                'verbose_name': 'Направление для обмена',
                'verbose_name_plural': 'Направления для обмена',
                'ordering': ['valute_from', 'valute_to'],
                'abstract': False,
                'unique_together': {('valute_from', 'valute_to')},
            },
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Название обменника')),
                ('xml_url', models.CharField(max_length=50, verbose_name='Ссылка на XML файл')),
                ('partner_link', models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Партнёрская ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус обменника')),
                ('period_for_update', models.IntegerField(blank=True, default=60, help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических обновлений', null=True, validators=[general_models.utils.model_validators.is_positive_validate], verbose_name='Частота обновлений в секундах')),
                ('direction_black_list', models.ManyToManyField(to='no_cash.direction', verbose_name='Чёрный список')),
            ],
            options={
                'verbose_name': 'Обменник',
                'verbose_name_plural': 'Обменники',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(default=None, max_length=50, null=True)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='no_cash.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.CharField(max_length=10, verbose_name='Отдаём')),
                ('valute_to', models.CharField(max_length=10, verbose_name='Получаем')),
                ('in_count', models.FloatField(verbose_name='Сколько отдаём')),
                ('out_count', models.FloatField(verbose_name='Сколько получаем')),
                ('min_amount', models.CharField(max_length=50, verbose_name='Минимальное количество')),
                ('max_amount', models.CharField(max_length=50, verbose_name='Максимальное количество')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directions', to='no_cash.exchange', verbose_name='Обменник')),
            ],
            options={
                'verbose_name': 'Готовое направление',
                'verbose_name_plural': 'Готовые направления',
                'ordering': ['exchange', 'valute_from', 'valute_to'],
                'unique_together': {('exchange', 'valute_from', 'valute_to')},
            },
        ),
    ]
