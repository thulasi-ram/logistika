from __future__ import unicode_literals

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        import notifications.signals
