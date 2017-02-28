from django.conf.urls import url

from organizations.views import OrganizationView, OrganizationList, OrganizationOnboardRequest

urlpatterns = [
    url(r'^list/$', OrganizationList.as_view(), name='list'),
    url(r'^onboard/$', OrganizationOnboardRequest.as_view(), name='onboard'),
    url(r'^(?P<org_name>[a-zA-Z0-9-_]+)/$', OrganizationView.as_view(), name='view'),

]