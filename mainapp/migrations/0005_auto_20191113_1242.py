# Generated by Django 2.2.6 on 2019-11-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_testmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testmodel',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='testmodel',
            name='title',
        ),
        migrations.AddField(
            model_name='testmodel',
            name='ean',
            field=models.CharField(default='ean', max_length=100),
        ),
        migrations.AddField(
            model_name='testmodel',
            name='lpformat',
            field=models.CharField(default='format', max_length=700),
        ),
    ]
