from __future__ import unicode_literals

from django.db import models
from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel


class Tenders(TimeStampedModel, CRUDPermissions):
    title = models.CharField(max_length=100)
    description = models.TextField()