# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-17 22:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duckmate', '0002_auto_20161017_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone_number',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='rental',
            name='address',
            field=models.CharField(max_length=500),
        ),
    ]
