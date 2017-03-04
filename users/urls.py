from django.conf.urls import url
from django.contrib.auth.views import password_reset_confirm
from django.urls import reverse_lazy

from users.views.change_password import ChangePassword
from users.views.forgot_password import ForgotPassword
from users.views.login import Login
from users.views.logout import Logout
from users.views.organization import UserOrganization
from users.views.profile import ProfileEdit
from users.views.signup import SignUp, SignupAPI

urlpatterns = [
    url(r'login', Login.as_view(), name='login'),
    url(r'api/signup/', SignupAPI.as_view(), name='signup-api'),
    url(r'signup', SignUp.as_view(), name='signup'),

    url(r'logout', Logout.as_view(), name='logout'),
    url(r'profile', ProfileEdit.as_view(), name='profile'),
    url(r'organization', UserOrganization.as_view(), name='organization'),
    url(r'^forgot/password/$', ForgotPassword.as_view(), name="password_reset"),
    url(r'^change-password/$', ChangePassword.as_view(), name="password_change"),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'post_reset_redirect': reverse_lazy('users:login')},
        name="password_reset_confirm"),
]