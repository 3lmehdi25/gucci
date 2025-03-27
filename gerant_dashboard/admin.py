from django.contrib import admin
from pdg_dashboard.models import Store, Stock, Order, Transaction

class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "gerant")

class StockAdmin(admin.ModelAdmin):
    list_display = ("item", "store", "quantity")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "store", "status")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("order", "store", "amount", "payment_method")

