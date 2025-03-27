from django import forms
from pdg_dashboard.models import User

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
