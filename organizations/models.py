from __future__ import unicode_literals

from django.db import models
from djutil.models import TimeStampedModel

from logistika.views.model_crud_permissions import CRUDPermissions


class Address(TimeStampedModel, CRUDPermissions):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.IntegerField()


class Organization(TimeStampedModel, CRUDPermissions):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    legal_address = models.ForeignKey(Address, null=True, related_name='legal_address')
    billing_address = models.ForeignKey(Address, null=True, related_name='billing_address')
    is_active = models.BooleanField(default=True)
