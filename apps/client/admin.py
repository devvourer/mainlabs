from django.contrib import admin

from .models import Bill, Organization, Client


admin.site.register(Client)
admin.site.register(Bill)
admin.site.register(Organization)
