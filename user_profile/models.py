from __future__ import unicode_literals

from django.db import models
from django.db.models import FileField

from logistika.views.model_crud_permissions import CRUDPermissions
from djutil.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _

from users.models import User


class Profile(TimeStampedModel, CRUDPermissions):
    user = models.OneToOneField(User, related_name='user')
    photo = FileField(verbose_name=_("Profile Picture"), upload_to='uploads/', null=True, blank=True)
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)