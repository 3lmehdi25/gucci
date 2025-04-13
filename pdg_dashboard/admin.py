from django.contrib import admin
from django.utils.html import format_html

from .models import Store, Category, Order, Stock, Expense, Dish, DishIngredient, Ingredient


class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1
    autocomplete_fields = ["ingredient"]  # Optionnel mais pratique
    min_num = 0


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "gerant", "created_at")
    search_fields = ("name", "location", "gerant__username")
    list_filter = ("gerant",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available", "dish_image")
    inlines = [DishIngredientInline]  # 👈 ajoute ça ici

    def dish_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" height="50" />')
        return "No Image"
    dish_image.short_description = "Image"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    search_fields = ("name",)

@admin.register(DishIngredient)
class DishIngredientAdmin(admin.ModelAdmin):
    list_display = ("dish", "ingredient", "quantity")
    search_fields = ("dish__name", "ingredient__name")


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


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("number", "store", "type", "category", "amount", "payment_status", "created_at")
    list_filter = ("type", "category", "payment_status", "store")
    search_fields = ("description",)
    readonly_fields = ("number", "created_at")
