from django.conf.urls import url

from organizations.views import OrganizationView

urlpatterns = [
    url(r'^(?P<org_name>[a-zA-Z0-9-_]+)/$', OrganizationView.as_view(), name='view'),
]