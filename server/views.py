from datetime import date

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

from server.forms import OrderEditForm


def is_server(user):
    return user.is_authenticated and user.role == "serveur"  # Check if user is a server



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone
from pdg_dashboard.models import Order, OrderDish, Dish, Store
from gerant_dashboard.models import MenuOfToday, MenuOfTodayDish, Table

from django.contrib import messages
@login_required
def create_order(request):
    store = request.user.store
    today = timezone.now().date()
    menu_today = store.menus_of_today.filter(date=today).first()

    if not menu_today:
        raise Http404("Aucun menu disponible pour aujourd’hui.")

    dishes_today = MenuOfTodayDish.objects.filter(menu_of_today=menu_today)
    tables = store.tables.all()

    # Get tables with active orders (not cancelled or completed)
    busy_table_ids = Order.objects.filter(
        store=store,
        status__in=["pending", "in_progress"],
        table__isnull=False
    ).values_list('table_id', flat=True)

    if request.method == "POST":
        order_type = request.POST.get("order_type", "takeaway")
        table_id = request.POST.get("table") if order_type == "dine_in" else None
        notes = request.POST.get("notes", "").strip()

        table = None
        if table_id:
            try:
                table = Table.objects.get(id=table_id, store=store)
                if int(table_id) in busy_table_ids:
                    messages.error(request, "Cette table est déjà occupée.")
                    raise ValueError("Busy table")
            except (Table.DoesNotExist, ValueError):
                return redirect("server:create_order")

        selected_dishes = []
        total_price = 0
        errors = []

        for item in dishes_today:
            dish_id = item.dish.id
            quantity_str = request.POST.get(f'dish_{dish_id}_quantity', '0')
            try:
                quantity = int(quantity_str)
            except ValueError:
                quantity = 0

            if quantity > 0:
                if quantity > item.remaining_quantity:
                    errors.append(f"Quantité invalide pour {item.dish.name} (max: {item.remaining_quantity})")
                else:
                    selected_dishes.append((item, quantity))
                    total_price += item.dish.price * quantity

        if not selected_dishes:
            errors.append("Vous devez sélectionner au moins un plat.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'server/order_form.html', {
                'dishes_today': dishes_today,
                'store': store,
                'today': today,
                'tables': tables,
                'busy_table_ids': list(busy_table_ids),
                'selected_type': order_type,
                'selected_table': table_id,
                'notes': notes,
            })

        order = Order.objects.create(
            store=store,
            status='pending',
            total_price=0,
            created_by=request.user,
            order_type=order_type,
            table=table,
            notes=notes
        )

        for item, quantity in selected_dishes:
            OrderDish.objects.create(
                order=order,
                dish=item.dish,
                quantity=quantity
            )
            item.sold_quantity += quantity
            item.save()

        order.total_price = total_price
        order.save()

        messages.success(request, "Commande créée avec succès.")
        return redirect('server:orders_list')

    return render(request, 'server/order_form.html', {
        'dishes_today': dishes_today,
        'store': store,
        'today': today,
        'tables': tables,
        'busy_table_ids': list(busy_table_ids),
    })

from django.utils import timezone
from gerant_dashboard.models import Reservation  # import the Reservation model

from django.utils import timezone
from gerant_dashboard.models import Reservation  # make sure this import exists

@login_required
def server_dashboard(request):
    if not is_server(request.user):
        return redirect("authentication:login")

    store = request.user.store
    today = timezone.now().date()

    orders = Order.objects.filter(store=store).exclude(status__in=['done', 'cancelled']).exclude(order_type="takeaway")

    reservations = Reservation.objects.filter(
        table__store=store,

    ).order_by('-date', 'time')

    context = {
        'orders': orders,
        'reservations': reservations,
        'store': store,
    }

    return render(request, 'server/orders_list.html', context)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status != 'done':
        # Restore dish quantities
        for order_dish in order.orderdish_set.all():
            try:
                menu_dish = MenuOfTodayDish.objects.get(
                    menu_of_today__date=order.created_at.date(),
                    menu_of_today__store=order.store,
                    dish=order_dish.dish
                )
                menu_dish.sold_quantity -= order_dish.quantity
                menu_dish.save()
            except MenuOfTodayDish.DoesNotExist:
                continue  # Just skip if the dish is no longer on today's menu

        order.status = 'cancelled'
        order.save()
        return redirect('server:orders_list')
    else:
        raise Http404("This order cannot be cancelled as it has already been paid.")




@login_required
def edit_order(request, order_id):
    # Get the order by ID
    order = get_object_or_404(Order, id=order_id, store=request.user.store)

    # Get dishes for the menu of today
    store = request.user.store
    today = timezone.now().date()
    menu_today = store.menus_of_today.filter(date=today).first()

    if not menu_today:
        raise Http404("No menu available for today.")

    dishes_today = MenuOfTodayDish.objects.filter(menu_of_today=menu_today)
    tables = store.tables.all()

    # Get current order's dish quantities
    dish_quantities = {order_dish.dish.id: order_dish.quantity for order_dish in order.dishes.all()}

    if request.method == "POST":
        order_type = request.POST.get("order_type", "takeaway")
        table_id = request.POST.get("table") if order_type == "dine_in" else None
        notes = request.POST.get("notes", "").strip()

        # Update table if applicable
        table = None
        if table_id:
            try:
                table = Table.objects.get(id=table_id, store=store)
            except Table.DoesNotExist:
                messages.error(request, "Table invalide.")
                return redirect("server:edit_order", order_id=order.id)

        # Update order details
        order.order_type = order_type
        order.table = table
        order.notes = notes
        order.save()

        # Update or add dishes to the order
        for item in dishes_today:
            dish_id = item.dish.id
            quantity_str = request.POST.get(f'dish_{dish_id}_quantity', '0')
            try:
                quantity = int(quantity_str)
            except ValueError:
                quantity = 0

            if quantity > 0:
                # Check if the dish exists in the current order
                order_dish, created = OrderDish.objects.update_or_create(
                    order=order, dish=item.dish, defaults={'quantity': quantity}
                )
                item.sold_quantity += quantity
                item.save()

        # After saving the changes, redirect to the orders list
        messages.success(request, "Commande mise à jour avec succès.")
        return redirect('server:orders_list')

    return render(request, 'server/edit_order.html', {
        'dishes_today': dishes_today,
        'store': store,
        'today': today,
        'tables': tables,
        'order': order,
        'selected_type': order.order_type,
        'selected_table': order.table.id if order.table else None,
        'notes': order.notes,
        'dish_quantities': dish_quantities
    })
