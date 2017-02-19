from django.conf.urls import url

from tenders.views import TendersFeed, CreateTender, ViewTender

urlpatterns = [
    url(r'^$', TendersFeed.as_view(), name='feed'),
    url(r'^create', CreateTender.as_view(), name='create'),
    url(r'^(?P<tender_id>[a-zA-Z0-9-_]+)/$', ViewTender.as_view(), name="view"),
]