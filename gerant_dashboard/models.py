from django.db import models
  # Assuming Table model is in gerant_dashboard
from pdg_dashboard.models import Store



class Table(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="tables")
    number = models.PositiveIntegerField()
    seats = models.PositiveIntegerField()  # Number of seats per table
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.number} - {self.store.name} ({self.seats} seats)"



class Reservation(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('not_reserved', 'Not Reserved'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="reservations")
    client_name = models.CharField(max_length=255)
    client_contact = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_reserved')

    def __str__(self):
        return f"Reservation for Table {self.table.number} on {self.date} at {self.time}"


class ReservationHistory(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    client_contact = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[("done", "Done"), ("canceled", "Canceled")])
    moved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historic Reservation for Table {self.table.number} on {self.date} at {self.time} - {self.status}"


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SpecialClient(models.Model):
    CLIENT_TYPES = [
        ("fidele", "Client fidèle"),
        ("enterprise", "Entreprise"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="special_client")
    type = models.CharField(max_length=20, choices=CLIENT_TYPES, default="simple")

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()}"