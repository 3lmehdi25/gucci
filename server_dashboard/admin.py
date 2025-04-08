from django.contrib import admin
from .models import Table, OrderStatus

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('store', 'number', 'capacity', 'is_available')
    search_fields = ('store__name', 'number')

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'server')
    list_filter = ('status', 'server')
    search_fields = ('order__id', 'server__username')
