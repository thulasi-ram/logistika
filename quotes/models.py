from __future__ import unicode_literals

from django.db import models
from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel

from tenders.models import Tenders
from users.models import User

class Quotes(TimeStampedModel, CRUDPermissions):
    tender = models.ForeignKey(to=Tenders,null=True)
    created_by = models.ForeignKey(to=User,null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    amount = models.DecimalField(max_digits=100, decimal_places=4)
    is_active = models.BooleanField(default=True)
