# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170227_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='static/images/account.png', upload_to='static/profile_images/'),
        ),
    ]
