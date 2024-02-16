from django.contrib import admin
from.models import (
    Deposit, 
    Withdrawal, 
    RecentTransaction,
    )


# Register your models here.

admin.site.register(Deposit)
admin.site.register(Withdrawal)
# admin.site.register(RecentTransaction)

