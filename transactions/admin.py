from django.contrib import admin
from.models import (
    Deposit, 
    Withdrawal, 
    RecentTransaction,
    )

class DepositAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'verified', 'date', 'reference']
    list_filter = ['user', 'verified', 'date']
    search_fields = ['user', 'verified', 'date']

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'verified', 'date', 'reference']
    list_filter = ['user', 'verified', 'date']
    search_fields = ['user', 'verified', 'date']

# Register your models here.

admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
# admin.site.register(RecentTransaction)

