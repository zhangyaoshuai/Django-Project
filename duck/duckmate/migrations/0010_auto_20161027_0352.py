# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duckmate', '0009_rental_coordinate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='picture',
            field=models.ImageField(default=None, height_field=150, upload_to=b'', width_field=200),
        ),
    ]