from __future__ import unicode_literals

from django.db import models
from djutil.models import TimeStampedModel

from logistika.views.model_crud_permissions import CRUDPermissions
from quotes.models import Quotes
from tenders.models import Tenders
from users.models import User


class TendersAudit(TimeStampedModel, CRUDPermissions):
    tender = models.ForeignKey(Tenders)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True)


class QuotesAudit(TimeStampedModel, CRUDPermissions):
    quote = models.ForeignKey(Quotes)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True)
