# forms.py
from django import forms
from pdg_dashboard.models import Order

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['notes']  # Only allowing notes to be edited for the order itself
