# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 03:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('duckmate', '0004_likedlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likedlist',
            name='user',
        ),
        migrations.AddField(
            model_name='rental',
            name='likes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rental',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(default=123, max_length=40),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='LikedList',
        ),
    ]
