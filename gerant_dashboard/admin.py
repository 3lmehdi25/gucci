from django.contrib import admin
from pdg_dashboard.models import Store, Stock, Order, Transaction
from django.contrib import admin
from .models import SpecialClient

class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "gerant")

class StockAdmin(admin.ModelAdmin):
    list_display = ("item", "store", "quantity")

class OrderAdmin(admin.ModelAdmin):
    list_display = ("client", "store", "status")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("order", "store", "amount", "payment_method")

from django import forms
from django.contrib import admin
from .models import SpecialClient
from django.contrib.auth import get_user_model

User = get_user_model()

# In gerant_dashboard/admin.py

from django import forms
from django.contrib import admin
from .models import SpecialClient
from django.contrib.auth import get_user_model

User = get_user_model()

class SpecialClientForm(forms.ModelForm):
    class Meta:
        model = SpecialClient
        fields = ['user', 'type']

    def __init__(self, *args, **kwargs):
        super(SpecialClientForm, self).__init__(*args, **kwargs)
        # Exclude users who are not clients or are already in SpecialClient as 'fidele' or 'enterprise'
        self.fields['user'].queryset = User.objects.filter(role='client').exclude(
            special_client__type__in=['fidele', 'enterprise']
        )  # Exclude 'fidele' and 'enterprise' clients

class SpecialClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', )
    list_filter = ('type',)
    search_fields = ('user__username',)
    form = SpecialClientForm  # Apply the custom form

admin.site.register(SpecialClient, SpecialClientAdmin)
