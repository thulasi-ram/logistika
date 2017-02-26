from __future__ import unicode_literals

from django.db import models
from djutil.models import TimeStampedModel

from logistika.views.model_crud_permissions import CRUDPermissions
from quotes.models import Quotes
from tenders.models import Tenders
from users.models import User


class TenderNotifications(TimeStampedModel, CRUDPermissions):
    READ = 1
    UNREAD = 0
    STATUS_CHOICES = ((READ, 'read'), (UNREAD, 'unread'))
    tender = models.ForeignKey(Tenders)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0)


class QuoteNotifications(TimeStampedModel, CRUDPermissions):
    READ = 1
    UNREAD = 0
    STATUS_CHOICES = ((READ, 'read'), (UNREAD, 'unread'))
    quote = models.ForeignKey(Quotes)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0)
