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
    position = models.CharField(max_length=50, choices=[("chef", "Chef"), ("server", "Serveur")])

    def __str__(self):
        return f"{self.user.username} - {self.position}"


class Order(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    client = models.ForeignKey("authentication.User", on_delete=models.CASCADE, limit_choices_to={"role": "client"})
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed")], default="pending")

    def __str__(self):
        return f"Order {self.id} - {self.client.username} ({self.store.name})"


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





