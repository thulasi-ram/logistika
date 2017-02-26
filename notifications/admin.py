from django.contrib import admin

# Register your models here.
from notifications.models import TenderNotifications, QuoteNotifications

admin.site.register(TenderNotifications)
admin.site.register(QuoteNotifications)