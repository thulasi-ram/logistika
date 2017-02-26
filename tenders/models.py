from __future__ import unicode_literals

from django.db import models
from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel

from users.models import User


class Tenders(TimeStampedModel, CRUDPermissions):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, null=True)
    is_active = models.BooleanField(default=True)

    def get_view_url(self):
        return "/{app_name}/{id}".format(app_name=self.__module__.split('.')[0], id=self.id)
