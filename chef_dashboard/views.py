from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

User = get_user_model()

def is_chef(user):
    return user.is_authenticated and user.role == "chef"

@login_required
def chef_dashboard(request):
    if not is_chef(request.user):
        return redirect("authentication:login")

    store = request.user.store  # or .managed_store if you're using that



    context = {
        "store": store,
    }
    return render(request, "chef_dashboard/home.html", context)



from pdg_dashboard.models import Dish, Order
from chef_dashboard.forms import DailyMenuForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from pdg_dashboard.models import Dish
from gerant_dashboard.models import DailyMenu, DailyMenuDish  # adjust as needed
from chef_dashboard.forms import DailyMenuForm  # or where your form is defined
from gerant_dashboard.models import DailyMenu, DailyMenuDish, MenuOfToday, MenuOfTodayDish  # ✅ add new models

@login_required
def declare_daily_menu(request):
    dishes = Dish.objects.all()

    if request.method == 'POST':
        form = DailyMenuForm(request.POST)
        if form.is_valid():
            daily_menu = form.save(commit=False)
            daily_menu.created_by = request.user
            daily_menu.store = request.user.store
            daily_menu.save()

            menu_dish_list = []  # store dishes added to DailyMenu

            for dish in dishes:
                checkbox = request.POST.get(f'dish_{dish.id}')
                quantity = request.POST.get(f'quantity_{dish.id}')

                if checkbox and quantity:
                    try:
                        quantity = int(quantity)
                        if quantity > 0:
                            DailyMenuDish.objects.create(
                                daily_menu=daily_menu,
                                dish=dish,
                                quantity=quantity
                            )
                            menu_dish_list.append((dish, quantity))
                    except ValueError:
                        continue

            # ✅ Create MenuOfToday automatically from DailyMenu
            menu_of_today = MenuOfToday.objects.create(
                store=request.user.store,
                generated_from=daily_menu,
                date=daily_menu.date
            )

            for dish, quantity in menu_dish_list:
                MenuOfTodayDish.objects.create(
                    menu_of_today=menu_of_today,
                    dish=dish,
                    initial_quantity=quantity,
                    sold_quantity=0  # by default
                )

            return redirect('chef_dashboard:home')
    else:
        form = DailyMenuForm()

    return render(request, 'chef_dashboard/declare_daily_menu.html', {
        'form': form,
        'dishes': dishes
    })
@login_required
def chef_orders_view(request):
    if not is_chef(request.user):
        return redirect("authentication:login")

    store = request.user.store


    # Exclude 'served', 'done', and 'cancelled'
    orders = Order.objects.filter(
        store=store,

    ).exclude(status__in=["done", "cancelled", "served"])

    return render(request, "chef_dashboard/chef_orders.html", {
        "orders": orders
    })

@require_POST
@login_required
def chef_update_order_status(request, order_id):
    if not is_chef(request.user):
        return redirect("authentication:login")

    order = get_object_or_404(Order, id=order_id, store=request.user.store)

    new_status = request.POST.get("status")
    if new_status and new_status != "done":
        order.status = new_status
        order.save()

    return redirect("chef_dashboard:chef_orders_view")