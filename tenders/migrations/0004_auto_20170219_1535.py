# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0003_tenders_is_disabled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenders',
            name='is_disabled',
        ),
        migrations.AddField(
            model_name='tenders',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
