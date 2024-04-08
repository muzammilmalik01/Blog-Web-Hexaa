from django.contrib import admin
from .models import CustomUser, PremiumUser


class AdminSite(admin.ModelAdmin):
    prepopulated_fields = {"username": ["email"]}


admin.site.register(
    CustomUser, AdminSite
)  # Registered the CustomUser in the Admin Section for CRUD Operatins.
admin.site.register(PremiumUser)
