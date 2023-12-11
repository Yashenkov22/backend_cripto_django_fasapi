# Generated by Django 4.2.7 on 2023-12-10 12:07

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
            name='BlackListElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('valute_from', models.CharField(max_length=10, verbose_name='Отдаём')),
                ('valute_to', models.CharField(max_length=10, verbose_name='Получаем')),
            ],
            options={
                'verbose_name': 'Элемент чёрного списка',
                'verbose_name_plural': 'Элементы чёрного списка',
                'ordering': ['city', 'valute_from', 'valute_to'],
                'unique_together': {('city', 'valute_from', 'valute_to')},
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Название страны')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('name',),
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
                ('direction_black_list', models.ManyToManyField(to='cash.blacklistelement', verbose_name='Чёрный список')),
            ],
            options={
                'verbose_name': 'Обменник',
                'verbose_name_plural': 'Обменники',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Название города')),
                ('code_name', models.CharField(max_length=10, unique=True, verbose_name='Кодовое имя')),
                ('is_parse', models.BooleanField(default=False, verbose_name='Статус парсинга')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='cash.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ['is_parse', 'name'],
            },
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
                ('is_active', models.BooleanField(default=True, verbose_name='Активно?')),
                ('city', models.CharField(max_length=100, verbose_name='Город')),
                ('fromfee', models.FloatField(blank=True, null=True, verbose_name='Процент')),
                ('params', models.CharField(blank=True, max_length=100, null=True, verbose_name='Параметры')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directions', to='cash.exchange', verbose_name='Обменник')),
            ],
            options={
                'verbose_name': 'Готовое направление',
                'verbose_name_plural': 'Готовые направления',
                'ordering': ['exchange', 'city', 'valute_from', 'valute_to'],
                'unique_together': {('exchange', 'city', 'valute_from', 'valute_to')},
            },
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_valutes_from', to='general_models.valute', to_field='code_name', verbose_name='Отдаём')),
                ('valute_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cash_valutes_to', to='general_models.valute', to_field='code_name', verbose_name='Получаем')),
            ],
            options={
                'verbose_name': 'Направление для обмена',
                'verbose_name_plural': 'Направления для обмена',
                'ordering': ['valute_from', 'valute_to'],
                'abstract': False,
                'unique_together': {('valute_from', 'valute_to')},
            },
        ),
    ]
