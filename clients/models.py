from __future__ import unicode_literals

from django.db import models
from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel

from users.models import User


class Clients(TimeStampedModel, CRUDPermissions):
    email = models.EmailField(max_length=100)
    created_by = models.ForeignKey(User, null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)


class ClientRequests(TimeStampedModel, CRUDPermissions):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    NOT_ACTED = ''
    STATUS_CHOICES = ((ACCEPTED, ACCEPTED), (REJECTED, REJECTED), (NOT_ACTED, NOT_ACTED))
    user = models.ForeignKey(User, related_name='invitee')
    invited_by = models.ForeignKey(User, related_name='inviter')
    status = models.CharField(default=NOT_ACTED, blank=True, choices=STATUS_CHOICES, max_length=20)

    def is_pending(self):
        return True if self.status == self.NOT_ACTED else False
