# Generated by Django 2.0 on 2021-02-24 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_nyaruka', '0005_auto_20210224_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='etat',
        ),
    ]