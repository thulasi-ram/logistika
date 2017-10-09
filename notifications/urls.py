from django.conf.urls import url

from notifications.views import NotificationsFeed

urlpatterns = [
    url(r'^$', NotificationsFeed.as_view(), name='feed'),
]