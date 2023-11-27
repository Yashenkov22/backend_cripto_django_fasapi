# Generated by Django 4.2.7 on 2023-11-25 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_exchangedirection_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exchangedirection',
            options={'ordering': ['exchange', 'valute_from', 'valute_to'], 'verbose_name': 'Готовое направление', 'verbose_name_plural': 'Готовые направления'},
        ),
        migrations.RenameField(
            model_name='exchangedirection',
            old_name='exchange_name',
            new_name='exchange',
        ),
        migrations.AlterUniqueTogether(
            name='exchangedirection',
            unique_together={('exchange', 'valute_from', 'valute_to')},
        ),
    ]
