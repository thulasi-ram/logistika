from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from djutil.models import TimeStampedModel

from logistika.views.model_crud_permissions import CRUDPermissions
from organizations.models import Organization
from quotes.models import Quotes
from tenders.models import Tenders
from users.models import User


class Notifications(TimeStampedModel, CRUDPermissions):
    READ = 1
    UNREAD = 0
    STATUS_CHOICES = ((READ, 'read'), (UNREAD, 'unread'))

    TENDER = 'tender'
    QUOTE = 'quote'
    USER = 'user'
    ORGANIZATION = 'organization'
    TYPE_CHOICES = ((TENDER, TENDER), (QUOTE, QUOTE), (USER, USER), (ORGANIZATION, ORGANIZATION))

    CREATED = 'has been created'
    MODIFIED = 'has been modified'
    DELETED = 'has been deleted'

    type = models.CharField(choices=TYPE_CHOICES, max_length=100)
    reference_id = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0)

    def get_message(self):
        try:
            referred_obj = self.get_referred_obj()
            return " {message} at {created_at:%Y-%m-%d %H:%M}".format(message=self.message, created_at=referred_obj.modified_at)
        except Exception as e:
            print e

    def get_referred_obj_factory(self):
        if self.type == self.TENDER:
            return Tenders
        elif self.type == self.QUOTE:
            return Quotes
        elif self.type == self.USER:
            return get_user_model()
        elif self.type== self.ORGANIZATION:
            return Organization

    def get_referred_obj(self):
        referred_model_klass = self.get_referred_obj_factory()
        return referred_model_klass.objects.get(id=self.reference_id)





