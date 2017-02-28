from django.contrib import admin

# Register your models here.
from organizations.models import Organization, Address, OrganizationOnboard, OrganizationRequests

admin.site.register(Organization)
admin.site.register(Address)
admin.site.register(OrganizationOnboard)
admin.site.register(OrganizationRequests)
