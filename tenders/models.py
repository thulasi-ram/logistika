from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel

from users.models import User


class Tenders(TimeStampedModel, CRUDPermissions):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, null=True)
    is_active = models.BooleanField(default=True)

    def get_view_url(self):
        return reverse('tenders:view', kwargs={'tender_id':self.id})
