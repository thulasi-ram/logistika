from django.conf.urls import url
from django.contrib.auth.views import password_reset_confirm
from django.urls import reverse_lazy

from quotes.views import QuotesConsolidated, CreateQuote
from users.views.forgot_password import ForgotPassword
from users.views.login import Login
from users.views.logout import Logout
from users.views.signup import SignUp

urlpatterns = [
    url(r'^$', QuotesConsolidated.as_view(), name='consolidated'),
    url(r'^create', CreateQuote.as_view(), name='create'),
    url(r'^compare', CreateQuote.as_view(), name='compare'),
]