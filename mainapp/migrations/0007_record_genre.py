# Generated by Django 2.2.7 on 2019-11-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20191123_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='genre',
            field=models.CharField(default='genre', max_length=200),
        ),
    ]