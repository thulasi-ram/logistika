from django.db import models


class CRUDPermissions(models.Model):
    class Meta:
        abstract = True
        default_permissions = ('add', 'change', 'delete', 'read')