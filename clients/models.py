from __future__ import unicode_literals

from django.db import models
from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel

from users.models import User


class Clients(TimeStampedModel, CRUDPermissions):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, null=True)