# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 04:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('bedroom', models.IntegerField(default=0)),
                ('bathroom', models.IntegerField(default=0)),
                ('coordinate', models.CharField(max_length=500)),
                ('picture', models.FileField(default=None, upload_to=b'')),
                ('is_favorite', models.BooleanField(default=False)),
                ('favorite_count', models.IntegerField(default=0)),
                ('phone_number', models.BigIntegerField(default=0)),
                ('email', models.EmailField(max_length=250)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=10)),
                ('student_type', models.CharField(choices=[('gra', 'graduate'), ('under', 'undergraduate'), ('employed', 'employed')], max_length=50)),
                ('major', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
