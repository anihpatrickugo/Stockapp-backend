from django.contrib import admin
from.models import (
    Deposit, 
    Withdrawal, 
    )


# Register your models here.

admin.site.register(Deposit)
admin.site.register(Withdrawal)
