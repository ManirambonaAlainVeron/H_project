# Generated by Django 2.0 on 2021-03-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_nyaruka', '0010_reports_colline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prise_charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Prise_charge',
            },
        ),
        migrations.CreateModel(
            name='Victime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_vict', models.CharField(max_length=50)),
                ('prenom_vict', models.CharField(max_length=50)),
                ('sexe_vict', models.CharField(max_length=50)),
                ('age_vict', models.IntegerField()),
                ('inter_age', models.CharField(max_length=50)),
                ('situation_phy_vict', models.CharField(max_length=50)),
                ('situation_psycho_vict', models.CharField(max_length=50)),
                ('statut_mart', models.CharField(max_length=50)),
                ('education_vict', models.CharField(max_length=50)),
                ('situation_psycho_auth', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Victime',
            },
        ),
    ]