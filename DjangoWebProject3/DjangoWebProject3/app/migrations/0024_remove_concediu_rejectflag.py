# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_concediu_rejectflag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concediu',
            name='rejectFlag',
        ),
    ]