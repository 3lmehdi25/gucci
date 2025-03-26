from django.contrib import admin
from django.utils.html import format_html

from .models import Store, MenuItem, Category, Order, Stock, Transaction

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "gerant", "created_at")
    search_fields = ("name", "location", "gerant__username")
    list_filter = ("gerant",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available", "menu_image")

    def menu_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"
    menu_image.short_description = "Image"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "store", "status", "created_at")
    list_filter = ("status", "store")
    search_fields = ("client__username",)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("item", "store", "quantity")
    search_fields = ("item",)
    list_filter = ("store",)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("order", "store", "amount", "payment_method", "timestamp")
    list_filter = ("store", "payment_method")
    search_fields = ("order__id",)
