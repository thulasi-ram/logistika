from django.conf.urls import url

from clients.views import ClientsFeed, CreateClient, ViewClient

urlpatterns = [
    url(r'^$', ClientsFeed.as_view(), name='feed'),
    url(r'^create', CreateClient.as_view(), name='create'),
    url(r'^(?P<client_id>[a-zA-Z0-9-_]+)/$', ViewClient.as_view(), name="view"),
]