from django.db import models

from django.db import models
from authentication.models import User



class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    gerant = models.OneToOneField(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"role": "gerant"},
        related_name="managed_store"  # This prevents the conflict
    )
    def __str__(self):
        return self.name

import os
from django.db import models
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



class Employee(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, choices=[("chef", "Chef"), ("server", "Serveur")])

    def __str__(self):
        return f"{self.user.username} - {self.position}"


# models.py in pdg_dashboard or gerant_dashboard (where Order model exists)
from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("in_kitchen", "En cuisine"),
        ("ready", "Prête"),
        ("served", "Servie"),
        ("cancelled", "Annulée"),
        ("done", "Terminée"),
    ]

    ORDER_TYPE_CHOICES = [
        ("dine_in", "Dine-in"),
        ("takeaway", "Takeaway"),
    ]

    client = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="orders")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    # New field for created_by
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="orders_created")

    # Many-to-many relationship for ordered dishes
    dishes = models.ManyToManyField('Dish', through='OrderDish')

    # New fields
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default="dine_in")
    table = models.ForeignKey('gerant_dashboard.Table', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.store.name} - {self.status}"




class OrderDish(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.dish.name} - {self.quantity} pcs"


class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item} ({self.quantity}) - {self.store.name}"

class Transaction(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="transactions")
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Each order creates one transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[("cash", "Cash"), ("card", "Credit/Debit Card"), ("online", "Online Payment")])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.store.name} ({self.amount} {self.payment_method})"







from django.db import models
from django.utils import timezone
from .models import Store

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('encaissement', 'Encaissement'),
        ('decaissement', 'Décaissement'),
    ]

    PAYMENT_STATUS = [
        ('paid', 'Payé'),
        ('unpaid', 'Non Payé'),

    ]

    CATEGORY_CHOICES = [
        ('facture', 'Facture'),
        ('salaire', 'Salaire'),
        ('order', 'Order'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="expenses")
    number = models.PositiveIntegerField(default=0)  # Manual numbering per store
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='paid')
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            # New object, assign next number for this store
            last_expense = Expense.objects.filter(store=self.store).order_by('-number').first()
            self.number = (last_expense.number + 1) if last_expense else 1
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.store.name} - {self.type} #{self.number}"

    class Meta:
        ordering = ['number']


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=20, default="g")  # Exemple: g, kg, L, etc.

    def __str__(self):
        return f"{self.name} ({self.unit})"












class Dish(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name="dishes")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="dishes")  # Chaque plat est lié à un restaurant
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_photos/", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.category.name} ({self.store.name})"


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantité nécessaire par plat (ex: 150g, 0.5L, etc.)")

    def __str__(self):
        return f"{self.dish.name} - {self.ingredient.name} ({self.quantity})"



    # Ensure image is deleted when a menu item is deleted
    @receiver(models.signals.post_delete, sender=dish)
    def delete_dish_image(sender, instance, **kwargs):
        if instance.image and os.path.isfile(instance.image.path):
            os.remove(instance.image.path)





class Supplier(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supplier_profile',
        limit_choices_to={'role': 'fournisseur'}  # Limiter le choix des utilisateurs à ceux ayant le rôle 'fournisseur'
    )
    name = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through="SupplierIngredient")

    def __str__(self):
        return f"{self.name}"




class SupplierIngredient(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.supplier.name} - {self.ingredient.name} ({self.quantity_needed} {self.ingredient.unit})"



# pdg_dashboard/models.py
from django.db import models
from .models import Ingredient, Supplier, Store
from django.utils import timezone

class SupplierIngredientRequest(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity_requested = models.FloatField()
    date_requested = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ("pending", "En attente"),
        ("approved", "Approuvée"),
        ("rejected", "Rejetée"),
        ("delivered", "Livrée")
    ], default="pending")

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity_requested} ({self.supplier.name})"




class SupplierResponse(models.Model):
    request = models.OneToOneField(SupplierIngredientRequest, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    date_responded = models.DateTimeField(auto_now=True)
