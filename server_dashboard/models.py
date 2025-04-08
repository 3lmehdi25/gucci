from django.db import models
from authentication.models import User
from pdg_dashboard.models import Store, Order


class Table(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.number} - {self.store.name}"


class OrderStatus(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("served", "Served")], default="pending")
    server = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={"role": "server"})

    def __str__(self):
        return f"Order {self.order.id} - {self.status}"
