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

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="menu_photos/", null=True, blank=True)  # Image field

    def __str__(self):
        return f"{self.name} ({self.category.name})"

# Ensure image is deleted when a menu item is deleted
@receiver(models.signals.post_delete, sender=MenuItem)
def delete_menu_item_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Employee(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, choices=[ ("chef_cuisinier", "Chef Cuisinier"), ("server", "Serveur")])

    def __str__(self):
        return f"{self.user.username} - {self.position}"


from django.db import models
from django.utils import timezone
from authentication.models import User
from pdg_dashboard.models import Store
from gerant_dashboard.models import Table

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("in_kitchen", "En cuisine"),
        ("ready", "Prête"),
        ("served", "Servie"),
        ("cancelled", "Annulée"),
        ("done", "Terminée"),
    ]

    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.store.name} - {self.status}"



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
        ('canceled', 'Annulé'),
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
