from django.conf.urls import url

from quotes.views import QuotesFeed, CreateQuote, ViewQuote

urlpatterns = [
    url(r'^$', QuotesFeed.as_view(), name='feed'),
    url(r'^create', CreateQuote.as_view(), name='create'),
    url(r'^shared', CreateQuote.as_view(), name='shared'),
    url(r'^(?P<quote_id>[a-zA-Z0-9-_]+)/$', ViewQuote.as_view(), name="view"),
]