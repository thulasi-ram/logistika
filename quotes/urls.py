from django.conf.urls import url

from quotes.views import QuotesFeed, CreateQuote

urlpatterns = [
    url(r'^$', QuotesFeed.as_view()),
    url(r'^create', CreateQuote.as_view(), name='create'),
]