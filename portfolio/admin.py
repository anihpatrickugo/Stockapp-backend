from django.contrib import admin
from.models import (
    Stock,
    Position
    )


# Register your models here.

admin.site.register(Stock)
admin.site.register(Position)


