# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 08:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_oohrequest_call_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oohrequest',
            name='call_time',
        ),
    ]
