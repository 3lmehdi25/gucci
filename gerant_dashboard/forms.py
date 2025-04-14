from django import forms

from django.forms.widgets import TimeInput, DateInput

from gerant_dashboard.models import Reservation, Table, SpecialClient
from pdg_dashboard.models import User, Stock

# Define valid roles for employees (excluding 'pdg' and 'gerant')
VALID_EMPLOYEE_ROLES = [
    ("caissier", "Caissier"),
    ("serveur", "Serveur"),
    ("chef", "Chef Cuisinier"),
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

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.role == "gerant":  # Check if the role is Gérant
            user.set_password("123")  # Set default password as '123' for Gérant
        else:
            user.set_password(user.password)  # Hash password for other roles

        if commit:
            user.save()
        return user
















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




from django import forms
from pdg_dashboard.models import Supplier, SupplierIngredient

class IngredientQuantityForm(forms.Form):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=True)
    ingredients_with_quantities = forms.CharField(widget=forms.HiddenInput(), required=True)

    def clean_ingredients_with_quantities(self):
        ingredients_with_quantities = self.cleaned_data.get('ingredients_with_quantities')
        return eval(ingredients_with_quantities)  # Convert the string back to a dict (ingredient_id: quantity)

from django import forms
from pdg_dashboard.models import Ingredient, Supplier, SupplierIngredient


class SupplierIngredientRequestForm(forms.Form):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.HiddenInput()
    )
    quantity = forms.FloatField(min_value=0.01, label="Quantité à commander")
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        label="Fournisseur"
    )

    def __init__(self, *args, **kwargs):
        ingredient_instance = kwargs.pop('ingredient', None)
        super().__init__(*args, **kwargs)

        if ingredient_instance:
            self.fields['ingredient'].initial = ingredient_instance
            # Restreindre les fournisseurs à ceux qui fournissent cet ingrédient
            self.fields['supplier'].queryset = Supplier.objects.filter(ingredients=ingredient_instance)










# gerant_dashboard/forms.py

from django import forms
from pdg_dashboard.models import Ingredient

class SupplierIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']  # Adjust fields based on your model


# forms.py
from django import forms
from pdg_dashboard.models import SupplierIngredient, Supplier
from pdg_dashboard.models import Ingredient

class SupplierIngredientForm(forms.ModelForm):
    class Meta:
        model = SupplierIngredient
        fields = ['ingredient', 'price_per_unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne montrer que les ingrédients existants (déjà créés par le PDG)
        self.fields['ingredient'].queryset = Ingredient.objects.all()


from django.forms import modelformset_factory

SupplierIngredientFormSet = modelformset_factory(
    SupplierIngredient,
    form=SupplierIngredientForm,
    extra=1,  # Important : ne pas afficher de champ au début
    can_delete=True  # (optionnel) # Tu peux ajuster selon le nombre d’ingrédients max à ajouter
)


