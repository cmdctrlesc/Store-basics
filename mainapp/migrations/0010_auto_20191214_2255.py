# Generated by Django 3.0 on 2019-12-14 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_record_coverimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='coverimage',
            field=models.ImageField(blank=True, null=True, upload_to='mainapp/coverimages'),
        ),
    ]
