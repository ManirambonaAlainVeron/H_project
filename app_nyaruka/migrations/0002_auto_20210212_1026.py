# Generated by Django 2.0 on 2021-02-12 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_nyaruka', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_cat', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'Categorie',
            },
        ),
        migrations.AlterField(
            model_name='commune',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_nyaruka.Province'),
        ),
        migrations.AddField(
            model_name='reports',
            name='categories',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app_nyaruka.Categorie'),
            preserve_default=False,
        ),
    ]
