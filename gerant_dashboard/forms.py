from django import forms

from django.forms.widgets import TimeInput, DateInput

from gerant_dashboard.models import Reservation, Table, SpecialClient
from pdg_dashboard.models import User, Stock

# Define valid roles for employees (excluding 'pdg' and 'gerant')
VALID_EMPLOYEE_ROLES = [
    ("caissier", "Caissier"),
    ("serveur", "Serveur"),
    ("chef_cuisinier", "Chef Cuisinier"),
    ("livreur", "Livreur"),
    ("fournisseur", "Fournisseur"),
    ("partenaire_professionnel", "Partenaire Professionnel"),
]

class EmployeeEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow roles from VALID_EMPLOYEE_ROLES
        self.fields["role"].choices = VALID_EMPLOYEE_ROLES


class EmployeeCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "role", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow roles from VALID_EMPLOYEE_ROLES
        self.fields["role"].choices = VALID_EMPLOYEE_ROLES

















class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["item", "quantity"]  # Store is auto-assigned






from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Reservation
        fields = [ 'client_name', 'client_contact', 'date', 'time']


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['seats']  # Removed 'number' since it's auto-generated


from django import forms
from django.contrib.auth import get_user_model
from .models import SpecialClient

User = get_user_model()

class SpecialClientForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role="client").exclude(
            special_client__type__in=["fidele", "enterprise"]
        ),
        label="Select Client",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    type = forms.ChoiceField(
        choices=SpecialClient.CLIENT_TYPES,
        label="Special Client Type",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = SpecialClient
        fields = ["user", "type"]


from django import forms
from pdg_dashboard.models import Expense






class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['store', 'created_at', 'number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially limit category field (overridden dynamically in template)
        self.fields['category'].choices = Expense.CATEGORY_CHOICES
# gerant_dashboard/forms.py
from django import forms
from gerant_dashboard.models import DailyMenu
from pdg_dashboard.models import Dish

class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ['date']
