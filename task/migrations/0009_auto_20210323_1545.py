# Generated by Django 3.1.7 on 2021-03-23 22:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_mytask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytask',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 15, 45, 11, 122404)),
        ),
        migrations.AlterField(
            model_name='mytask',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]