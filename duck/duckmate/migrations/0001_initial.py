# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-17 20:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(default=0)),
                ('email', models.EmailField(max_length=250)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=10)),
                ('student_type', models.CharField(default='gra', max_length=50)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=0)),
                ('bedroom', models.IntegerField(default=1)),
                ('bathroom', models.IntegerField(default=1)),
                ('coordinate', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('picture', models.ImageField(height_field=200, upload_to=b'', width_field=200)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='duckmate.Contact')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
