# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0004_auto_20170426_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offering',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='offering',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]