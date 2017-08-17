# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 08:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_oohrequest_call_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='oohrequest',
            name='call_time',
            field=models.TimeField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
