# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20170808_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oohrequest',
            name='call_time',
            field=models.TimeField(),
        ),
    ]
