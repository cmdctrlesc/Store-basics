# Generated by Django 2.2.6 on 2019-11-05 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.Label'),
        ),
    ]
