# gerant_dashboard/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from pdg_dashboard.models import Supplier  # adapte selon l'endroit où tu définis Supplier

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_supplier_for_fournisseur(sender, instance, created, **kwargs):
    if created and instance.role == "fournisseur":
        # Vérifie que ce user n’a pas déjà un fournisseur
        Supplier.objects.get_or_create(user=instance,name=instance.username)
