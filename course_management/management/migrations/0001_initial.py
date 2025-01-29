# Generated by Django 5.1.4 on 2025-01-29 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('units', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4')])),
                ('department', models.CharField(max_length=100)),
                ('instructor', models.CharField(max_length=100)),
                ('days', models.CharField(max_length=50)),
                ('time', models.CharField(max_length=50)),
                ('exam_datetime', models.DateTimeField()),
            ],
        ),
    ]
