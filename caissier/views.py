from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from pdg_dashboard.models import Order, Expense  # Make sure Order and Expense are imported

def is_caissier(user):
    return user.is_authenticated and user.role == "caissier"

@login_required
def caissier_home(request):
    if not is_caissier(request.user):
        return redirect("authentication:login")

    return render(request, "caissier/home.html")


@login_required
def served_orders(request):
    if not is_caissier(request.user):
        return redirect("authentication:login")

    store = request.user.store
    dine_in_orders = Order.objects.filter(store=store, status="served", order_type="dine_in")
    takeaway_orders = Order.objects.filter(store=store, status="served", order_type="takeaway")

    return render(request, "caissier/served_orders.html", {
        "dine_in_orders": dine_in_orders,
        "takeaway_orders": takeaway_orders
    })



@login_required
def order_detail(request, order_id):
    if not is_caissier(request.user):
        return redirect("authentication:login")

    order = get_object_or_404(Order, id=order_id, store=request.user.store)
    return render(request, "caissier/order_detail.html", {"order": order})


@require_POST
@login_required
def mark_order_done(request, order_id):
    if not is_caissier(request.user):
        return redirect("authentication:login")

    order = get_object_or_404(Order, id=order_id, store=request.user.store)

    if order.status == "served":
        order.status = "done"
        order.save()

        Expense.objects.create(
            store=order.store,
            amount=order.total_price,
            type="encaissement",
            category="order",
            payment_status="paid",
            description=f"Paiement de la commande #{order.id}"
        )

    return redirect("caissier:served_orders")
