# Generated by Django 3.0 on 2020-02-23 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_record_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(default='position', max_length=100, null=True)),
                ('name', models.CharField(default='songname', max_length=800, null=True)),
                ('duration', models.CharField(default='position', max_length=100, null=True)),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Record')),
            ],
        ),
    ]