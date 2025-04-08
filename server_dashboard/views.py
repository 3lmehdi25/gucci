from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Order, Table
from django.contrib import messages


@login_required
def pending_orders(request):
    """ Affiche les commandes en attente pour le serveur """
    if request.user.role != 'serveur':
        return HttpResponseForbidden("Accès interdit")  # Si l'utilisateur n'est pas un serveur

    # Récupérer les commandes en attente de la boutique du serveur
    orders = Order.objects.filter(status='pending', store=request.user.managed_store)

    # Afficher les commandes dans la vue
    return render(request, 'server_dashboard/pending_orders.html', {'orders': orders})


@login_required
def mark_as_served(request, order_id):
    """ Permet au serveur de marquer une commande comme servie """
    if request.user.role != 'serveur':
        return HttpResponseForbidden("Accès interdit")  # Si l'utilisateur n'est pas un serveur

    # Récupérer l'order
    try:
        order = Order.objects.get(id=order_id, store=request.user.managed_store, status='pending')
    except Order.DoesNotExist:
        messages.error(request, "Commande introuvable ou déjà servie.")
        return redirect('server_dashboard:pending_orders')

    # Marquer la commande comme servie
    order.status = 'completed'
    order.save()

    # Optionnellement, tu peux envoyer une notification au client ici (si tu as un système de notification)

    messages.success(request, f"La commande {order.id} a été marquée comme servie.")
    return redirect('server_dashboard:pending_orders')


@login_required
def assigned_tables(request):
    """ Affiche les tables assignées au serveur ou au restaurant """
    if request.user.role != 'serveur':
        return HttpResponseForbidden("Accès interdit")  # Si l'utilisateur n'est pas un serveur

    # Récupérer les tables assignées au serveur (ou à son restaurant)
    tables = Table.objects.filter(store=request.user.managed_store)

    # Afficher les tables dans la vue
    return render(request, 'server_dashboard/assigned_tables.html', {'tables': tables})
