from django import forms
from gerant_dashboard.models import DailyMenu
from pdg_dashboard.models import Dish

class DailyMenuForm(forms.ModelForm):
    class Meta:
        model = DailyMenu
        fields = ['date']