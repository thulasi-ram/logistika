from django.dispatch import receiver

from audit.models import TendersAudit
from tenders.signals import tender_created, tender_modified, tender_deleted


@receiver(tender_created)
def tender_created(sender, instance, user, **kwargs):
    TendersAudit.objects.create(tender=instance, message='create', user=user)


@receiver(tender_modified)
def tender_modified(sender, instance, user, **kwargs):
    TendersAudit.objects.create(tender=instance, message='modififed', user=user)


@receiver(tender_deleted)
def tender_deleted(sender, instance, user, **kwargs):
    TendersAudit.objects.create(tender=instance, message='deleted', user=user)
