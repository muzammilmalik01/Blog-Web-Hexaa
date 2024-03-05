from django.contrib import admin
from .models import CustomUser

class AdminSite(admin.ModelAdmin):
    prepopulated_fields = {'username':['email']}

admin.site.register(CustomUser,AdminSite) # Registered the CustomUser in the Admin Section for CRUD Operatins.
