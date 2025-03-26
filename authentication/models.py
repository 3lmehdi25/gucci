from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("pdg", "PDG"),
        ("gerant", "Gérant"),
        ("client", "Client"),
        ("chef", "Chef Cuisinier"),
        ("serveur", "Serveur"),
        ("livreur", "Livreur"),
        ("caissier", "Caissier"),
        ("partenaire", "Partenaire Professionnel"),
        ("fournisseur", "Fournisseur"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")
    store = models.ForeignKey(
        "pdg_dashboard.Store",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="employees"  # This prevents the conflict
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
