from django.contrib import admin

# Register your models here.
from quotes.models import Quotes

admin.site.register(Quotes)
