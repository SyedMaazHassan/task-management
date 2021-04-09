# Generated by Django 3.1.7 on 2021-03-24 08:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0011_auto_20210323_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytask',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 24, 1, 6, 35, 230682)),
        ),
        migrations.CreateModel(
            name='myNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_text', models.TextField()),
                ('created_on', models.DateTimeField(default=datetime.datetime(2021, 3, 24, 1, 6, 35, 231684))),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('added_for', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='task.customer')),
            ],
        ),
    ]
