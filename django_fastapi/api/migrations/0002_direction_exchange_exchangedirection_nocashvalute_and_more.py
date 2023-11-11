# Generated by Django 4.2.7 on 2023-11-10 04:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('xml_url', models.CharField(max_length=50)),
                ('partner_link', models.CharField(blank=True, default=None, max_length=50, null=True)),
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
                ('min_amount', models.FloatField()),
                ('max_amount', models.FloatField()),
                ('exchange_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='NoCashValute',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('code_name', models.CharField(max_length=10, unique=True)),
                ('type_valute', models.CharField(choices=[('cripto', 'Криптовалюта'), ('elecro_money', 'Электронные деньги'), ('exchange_balance', 'Балансы криптобирж'), ('internet_banking', 'Интернет-банкинг'), ('money_transfer', 'Денежные переводы')], max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.AddField(
            model_name='direction',
            name='valute_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valutes_from', to='api.nocashvalute'),
        ),
        migrations.AddField(
            model_name='direction',
            name='valute_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='valutes_to', to='api.nocashvalute'),
        ),
    ]
