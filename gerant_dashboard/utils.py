from pdg_dashboard.models import Order
from .models import SpecialClient
from django.db import models

FIDELITY_ORDER_COUNT = 50
FIDELITY_SPENDING_AMOUNT = 100_000  # en DA


def check_and_update_client_fidelity(user):
    """
    Vérifie si un utilisateur devient un client fidèle et met à jour son statut.
    La création d'un SpecialClient se fait uniquement si les conditions de fidélité sont remplies.
    """

    # Ne rien faire si l'utilisateur est déjà une entreprise
    try:
        special_client = user.special_client
        if special_client.type == "enterprise":
            return
    except SpecialClient.DoesNotExist:
        # Si l'utilisateur n'a pas de SpecialClient, vérifier si les conditions sont remplies
        total_orders, total_spent = Order.objects.filter(client=user).aggregate(
            order_count=models.Count('id'),
            total_spent=models.Sum('total_price')
        ).values()

        total_spent = total_spent or 0  # Si aucun montant total n'est trouvé, assigne 0

        # Vérification des critères de fidélité (50 commandes ou 100 000 DA dépensés)
        if total_orders >= FIDELITY_ORDER_COUNT or total_spent >= FIDELITY_SPENDING_AMOUNT:
            # Créer un SpecialClient de type "fidele" si conditions sont remplies
            SpecialClient.objects.create(user=user, type="fidele")




# gerant_dashboard/utils.py

from collections import defaultdict

def calculate_ingredient_needs(daily_menu):
    """
    Retourne un dictionnaire {ingredient: quantité totale nécessaire}
    basé sur les plats et quantités du menu journalier.
    """
    from pdg_dashboard.models import DishIngredient

    ingredient_totals = defaultdict(float)

    for daily_dish in daily_menu.dailymenudish_set.select_related('dish'):
        dish = daily_dish.dish
        quantity = daily_dish.quantity

        for dish_ingredient in DishIngredient.objects.filter(dish=dish).select_related('ingredient'):
            ingredient = dish_ingredient.ingredient
            needed = dish_ingredient.quantity * quantity
            ingredient_totals[ingredient] += needed

    return ingredient_totals
