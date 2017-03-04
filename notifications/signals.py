from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notifications
from organizations.models import OrganizationRequests
from tenders.signals import tender_created, tender_modified, tender_deleted
from users.models import Roles


@receiver(tender_created)
def tender_created(sender, instance, user, **kwargs):
    Notifications.objects.create(type='tender', message=' has been created', user=instance.created_by, reference_id=instance.id)


@receiver(tender_modified)
def tender_modified(sender, instance, user, **kwargs):
    audit_log_users = list(instance.tendersaudit_set.values_list('user_id', flat=True))
    quotes_users = list(instance.quotes_set.values_list('created_by', flat=True))
    for usr in set(audit_log_users + quotes_users + [instance.created_by.id]):
        Notifications.objects.create(type='tender', message=' has been modified', user_id=usr, reference_id=instance.id)


@receiver(tender_deleted)
def tender_deleted(sender, instance, user, **kwargs):
    audit_log_users = list(instance.tendersaudit_set.values_list('user_id', flat=True))
    quotes_users = list(instance.quotes_set.values_list('created_by', flat=True))
    for usr in set(audit_log_users + quotes_users + [instance.created_by.id]):
        Notifications.objects.create(type='tender', message=' has been deleted', user_id=usr, reference_id=instance.id)


@receiver(post_save, sender=OrganizationRequests)
def org_req_save(sender, instance, created, *args, **kwargs):
    if created:
        users = get_user_model().objects.filter(organization=instance.org, role_id=Roles.ADMIN)
        for usr in users:
            Notifications.objects.create(type='user', message=' has requested to be part of your organization',
                                         user=usr, reference_id=instance.id)
    else:
        Notifications.objects.create(type='organization',
                                     message=' has {req_status} your request.'.format(req_status=instance.status),
                                     user=instance.user, reference_id=instance.user.id)
