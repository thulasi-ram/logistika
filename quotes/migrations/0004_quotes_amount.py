# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_quotes_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='amount',
            field=models.DecimalField(decimal_places=4, default=1, max_digits=100),
            preserve_default=False,
        ),
    ]
