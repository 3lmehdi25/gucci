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




# models.py dans gerant_dashboard

from django.utils import timezone
from django.db import models
from django.utils import timezone
from pdg_dashboard.models import Store, Dish
from authentication.models import User  # or wherever your custom User model is

class DailyMenu(models.Model):
    date = models.DateField(default=timezone.now, unique=False)  # remove global uniqueness
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'gerant'}
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="daily_menus")
    dishes = models.ManyToManyField(Dish, through="DailyMenuDish")

    class Meta:
        unique_together = ('date', 'store')  # Ensures one menu per store per day

    def __str__(self):
        return f"Menu du {self.date} ({self.store.name})"



class DailyMenuDish(models.Model):
    daily_menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    dish = models.ForeignKey("pdg_dashboard.Dish", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Nombre de portions prévues

    class Meta:
        unique_together = ('daily_menu', 'dish')


class MenuOfToday(models.Model):
    date = models.DateField(default=timezone.now)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="menus_of_today")
    generated_from = models.OneToOneField(DailyMenu, on_delete=models.CASCADE, related_name="menu_of_today")

    class Meta:
        unique_together = ('date', 'store')

    def __str__(self):
        return f"Menu of Today - {self.date} ({self.store.name})"


class MenuOfTodayDish(models.Model):
    menu_of_today = models.ForeignKey(MenuOfToday, on_delete=models.CASCADE, related_name="dishes")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    initial_quantity = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('menu_of_today', 'dish')

    @property
    def remaining_quantity(self):
        return self.initial_quantity - self.sold_quantity

    def __str__(self):
        return f"{self.dish.name} - {self.remaining_quantity()} remaining"




