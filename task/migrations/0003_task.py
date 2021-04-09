# Generated by Django 3.1.6 on 2021-03-17 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_customer_added_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField()),
                ('task_due_date', models.DateTimeField(auto_now_add=True)),
                ('task', models.CharField(max_length=100)),
            ],
        ),
    ]
