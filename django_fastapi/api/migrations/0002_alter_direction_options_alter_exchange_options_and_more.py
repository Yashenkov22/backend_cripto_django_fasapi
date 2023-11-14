# Generated by Django 4.2.7 on 2023-11-13 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='direction',
            options={'verbose_name': 'Направление для обмена', 'verbose_name_plural': 'Направления для обмена'},
        ),
        migrations.AlterModelOptions(
            name='exchange',
            options={'verbose_name': 'Обменник', 'verbose_name_plural': 'Обменники'},
        ),
        migrations.AlterModelOptions(
            name='exchangedirection',
            options={'verbose_name': 'Направление из обменника', 'verbose_name_plural': 'Направления из обменников'},
        ),
        migrations.AlterModelOptions(
            name='nocashvalute',
            options={'verbose_name': 'Безналичная валюта', 'verbose_name_plural': 'Безналичные валюты'},
        ),
        migrations.RemoveField(
            model_name='direction',
            name='direction_name',
        ),
        migrations.AlterField(
            model_name='direction',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='exchangedirection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
