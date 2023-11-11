# Generated by Django 4.2.7 on 2023-11-11 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('xml_url', models.CharField(max_length=50)),
                ('partner_link', models.CharField(blank=True, default=None, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoCashValute',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('code_name', models.CharField(max_length=10, unique=True)),
                ('type_valute', models.CharField(choices=[('Криптовалюта', 'Криптовалюта'), ('Электронные деньги', 'Электронные деньги'), ('Балансы криптобирж', 'Балансы криптобирж'), ('Интернет-банкинг', 'Интернет-банкинг'), ('Денежные переводы', 'Денежные переводы')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('exchange_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('rating', models.CharField(default=None, max_length=50, null=True)),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeDirection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valute_from', models.CharField(max_length=10)),
                ('valute_to', models.CharField(max_length=10)),
                ('in_count', models.FloatField()),
                ('out_count', models.FloatField()),
                ('min_amount', models.CharField(max_length=50)),
                ('max_amount', models.CharField(max_length=50)),
                ('exchange_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction_name', models.CharField(max_length=20, unique=True)),
                ('valute_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valutes_from', to='api.nocashvalute', to_field='code_name')),
                ('valute_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valutes_to', to='api.nocashvalute', to_field='code_name')),
            ],
            options={
                'unique_together': {('valute_from', 'valute_to')},
            },
        ),
    ]
