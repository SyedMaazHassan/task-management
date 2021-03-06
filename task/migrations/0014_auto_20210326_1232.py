# Generated by Django 3.1.7 on 2021-03-26 19:32

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0013_auto_20210325_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='renewal_date',
            field=models.DateField(default=datetime.date(2021, 3, 26)),
        ),
        migrations.AlterField(
            model_name='mynote',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 12, 32, 13, 938009)),
        ),
        migrations.AlterField(
            model_name='mytask',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 12, 32, 13, 937009)),
        ),
        migrations.CreateModel(
            name='myFieldValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.customer')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='myField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255)),
                ('field_type', models.CharField(max_length=255)),
                ('is_requied', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='dynamicFieldStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
