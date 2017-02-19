from django.conf.urls import url

from tenders.views import TendersFeed, CreateTender

urlpatterns = [
    url(r'^$', TendersFeed.as_view(), name='feed'),
    url(r'^create', CreateTender.as_view(), name='create'),
]