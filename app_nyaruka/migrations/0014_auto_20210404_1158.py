# Generated by Django 2.0 on 2021-04-04 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_nyaruka', '0013_victime_date_evenement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reports',
            name='date_mes',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reports',
            name='heure_mes',
            field=models.TimeField(),
        ),
    ]
