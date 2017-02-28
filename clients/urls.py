from django.conf.urls import url

from clients.views import ClientsFeed, InviteClient, ViewClient, ClientRequestsView

urlpatterns = [
    url(r'^$', ClientsFeed.as_view(), name='feed'),
    url(r'^invite', InviteClient.as_view(), name='invite'),
    url(r'^requests', ClientRequestsView.as_view(), name='requests'),
    url(r'^(?P<client_id>[a-zA-Z0-9-_]+)/$', ViewClient.as_view(), name="view"),
]