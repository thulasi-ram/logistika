from django.contrib import admin

# Register your models here.
from audit.models import TendersAudit, QuotesAudit

admin.site.register(TendersAudit)
admin.site.register(QuotesAudit)