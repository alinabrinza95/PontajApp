# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20170808_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oohrequest',
            name='incident_number',
            field=models.CharField(max_length=100),
        ),
    ]
