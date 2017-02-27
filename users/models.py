from __future__ import unicode_literals

import hashlib
import random

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djutil.models import TimeStampedModel

from logistika.views.model_crud_permissions import CRUDPermissions
from organizations.models import Organization
from users.views.user_manager import CustomUserManager


class Roles(TimeStampedModel, CRUDPermissions):
    role_name = models.CharField(max_length=100)
    role_code = models.CharField(max_length=100)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, CRUDPermissions):
    first_name = models.CharField(_('First Name'), max_length=254)
    last_name = models.CharField(_('Last Name'), max_length=254, blank=True, default="")

    email = models.EmailField(_('email address'), max_length=254, unique=True)
    username = models.CharField(_('user name'), max_length=254, unique=True)
    phone_number = models.CharField(_('phone_number'), max_length=20, blank=True, default="")

    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_(
        'Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.'))

    is_confirmed = models.BooleanField(_('is confirmed'), default=False)
    confrmation_key = models.CharField(max_length=40)
    organization = models.ForeignKey(Organization, null=True)
    role = models.ForeignKey(Roles, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta(CRUDPermissions.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name.strip()

    def email_user(self, subject, message, from_email=None):
        from_email = settings.SERVER_EMAIL
        send_mail(subject, message, from_email, [self.email])

    def set_confirmation_key(self, email):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        self.confrmation_key = hashlib.sha1(salt + email).hexdigest()

    def get_profile_context(self):
        return {'profile_url': self.get_profile_image_url()}

    def get_profile_initial(self):
        return {'phone': self.phone_number,
                'first_name': self.first_name,
                'last_name': self.last_name}

    def get_profile_image_url(self):
        try:
            return self.profile.photo
        except:
            return ''
    @property
    def is_admin(self):
        return self.is_staff


class Profile(TimeStampedModel, CRUDPermissions):
    user = models.OneToOneField(User, related_name='profile')
    photo = models.ImageField(upload_to='profile_images/', default='profile_images/account.png')
    website = models.URLField(default='', blank=True)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    organization = models.CharField(max_length=100, default='', blank=True)
