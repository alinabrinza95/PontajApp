# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_pontaj_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='concediu',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
