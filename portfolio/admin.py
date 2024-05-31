from django.contrib import admin
from.models import (
    Stock,
    Position
    )

class StockAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name', 'price', 'open', 'market_cap')
    search_fields = ('ticker', 'name', 'price', 'market_cap')
    list_filter = ('ticker', 'name', 'price', 'market_cap')
    ordering = ('ticker', 'name', 'price', 'market_cap')


# Register your models here.

admin.site.register(Stock, StockAdmin)
admin.site.register(Position)


