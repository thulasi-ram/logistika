from django.contrib import admin

# Register your models here.
from clients.models import Clients, ClientRequests

admin.site.register(Clients)
admin.site.register(ClientRequests)