# Generated by Django 4.2.7 on 2023-11-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_direction_valute_from_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangedirection',
            name='max_amount',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='exchangedirection',
            name='min_amount',
            field=models.CharField(max_length=50),
        ),
    ]
