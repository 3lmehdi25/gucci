from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        """Filter role choices: PDG cannot be created manually."""
        form = super().get_form(request, obj, **kwargs)
        allowed_roles = [
            ("gerant", "Gérant"),
            ("chef", "Chef Cuisinier"),
            ("serveur", "Serveur"),
            ("livreur", "Livreur"),
            ("caissier", "Caissier"),
            ("partenaire", "Partenaire Professionnel"),
            ("fournisseur", "Fournisseur"),
        ]
        if not obj:  # When creating a new user, restrict role choices
            form.base_fields["role"].choices = allowed_roles
        return form
    list_display = ("username", "email", "role", "store")
    search_fields = ("username", "email")
    list_filter = ("role", "store")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Role & Store", {"fields": ("role", "store")} ),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "store"),
        }),
    )

    def get_queryset(self, request):
        """Exclude clients from the admin user list."""
        queryset = super().get_queryset(request)
        return queryset.exclude(role="client")

    def get_readonly_fields(self, request, obj=None):
        """Prevent clients from having a store assigned."""
        if obj and obj.role == "client":
            return ["store"]
        return []

admin.site.register(User, CustomUserAdmin)
