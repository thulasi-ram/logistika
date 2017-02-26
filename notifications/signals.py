from django.dispatch import receiver

from notifications.models import Notifications
from tenders.signals import tender_created, tender_modified, tender_deleted


@receiver(tender_created)
def tender_created(sender, instance, user, **kwargs):
    Notifications.objects.create(type='tender', message=' has been created', user=instance.created_by)


@receiver(tender_modified)
def tender_modified(sender, instance, user, **kwargs):
    audit_log_users = list(instance.tendersaudit_set.values_list('user_id', flat=True))
    quotes_users = list(instance.quotes_set.values_list('created_by', flat=True))
    for usr in set(audit_log_users + quotes_users + [instance.created_by.id]):
        Notifications.objects.create(type='tender', message=' has been modified', user_id=usr)


@receiver(tender_deleted)
def tender_deleted(sender, instance, user, **kwargs):
    audit_log_users = list(instance.tendersaudit_set.values_list('user_id', flat=True))
    quotes_users = list(instance.quotes_set.values_list('created_by', flat=True))
    for usr in set(audit_log_users + quotes_users + [instance.created_by.id]):
        Notifications.objects.create(type='tender', message=' has been deleted', user_id=usr)
