from django.conf.urls import url

from clients.views import ClientsFeed, CreateClient

urlpatterns = [
    url(r'^$', ClientsFeed.as_view(), name='feed'),
    url(r'^create', CreateClient.as_view(), name='create'),
]