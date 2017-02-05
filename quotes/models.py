from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Quotes(models.Model):
    title = models.CharField(max_length=100)