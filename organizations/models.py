from __future__ import unicode_literals

from django.conf import settings
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


class OrganizationOnboard(TimeStampedModel, CRUDPermissions):
    PENDING = 'pending'
    ONBOARDED = 'onboarded'
    STATUS_CHOICES = ((PENDING, PENDING), (ONBOARDED, ONBOARDED))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    address = models.TextField()
    telephone = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class OrganizationRequests(TimeStampedModel, CRUDPermissions):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    NOT_ACTED = ''
    STATUS_CHOICES = ((ACCEPTED, ACCEPTED), (REJECTED, REJECTED), (NOT_ACTED, NOT_ACTED))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    org = models.ForeignKey(Organization, related_name='org')
    status = models.CharField(default=NOT_ACTED, blank=True, choices=STATUS_CHOICES, max_length=20)

    def is_pending(self):
        return True if self.status == self.NOT_ACTED else False

    def is_rejected(self):
        return True if self.status == self.REJECTED else False