from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'balance', 'wallet_address', 'photo', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'balance', 'wallet_address',)
    list_filter = ('is_active', 'is_staff')
    ordering = ('first_name', 'last_name', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
