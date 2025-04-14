from datetime import date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from pdg_dashboard.models import Store, Stock
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import User
from pdg_dashboard.models import Store
from .forms import EmployeeEditForm, EmployeeCreateForm, StockForm, TableForm, ReservationForm, SpecialClientForm
from .models import Reservation, Table, ReservationHistory, SpecialClient
from django.contrib.auth import get_user_model

User = get_user_model()  # This ensures you're using 'authentication.User'

def is_gerant(user):
    """Check if the user is a Gérant."""
    return user.is_authenticated and user.role == "gerant"

@login_required
def gerant_dashboard(request):
    """Main dashboard for Gérant, showing store overview."""
    if not is_gerant(request.user):
        return redirect("authentication:login")  # Redirect if not Gérant

    store = request.user.managed_store  # Get the store assigned to the Gérant

    context = {
        "store": store,
    }
    return render(request, "gerant_dashboard/home.html", context)
@login_required
def manage_employees(request):
    # Get the store of the currently logged-in Gérant
    gerant_store = request.user.store

    # List only employees in the same store, excluding 'pdg' and 'gerant'
    employees = User.objects.filter(store=gerant_store).exclude(role__in=["pdg", "gerant"])

    return render(request, "gerant_dashboard/manage_employees.html", {"employees": employees})

@login_required
def add_employee(request):
    """Gérant can add new employees to their store."""
    if not is_gerant(request.user):
        return redirect("authentication:login")

    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.store = request.user.managed_store  # Assign store
            employee.save()
            messages.success(request, "Employee added successfully!")
            return redirect("gerant_dashboard:manage_employees")
    else:
        form = EmployeeCreateForm()

    return render(request, "gerant_dashboard/add_employee.html", {"form": form})

@login_required
def delete_employee(request, employee_id):
    """Gérant can remove an employee (except other Gérants)."""
    if not is_gerant(request.user):
        return redirect("authentication:login")

    employee = get_object_or_404(User, id=employee_id, store=request.user.managed_store)

    if employee.role == "gerant":  # Prevent deleting another Gérant
        messages.error(request, "You cannot remove another Gérant.")
    else:
        employee.delete()
        messages.success(request, "Employee removed successfully!")

    return redirect("gerant_dashboard:manage_employees")
@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(User, id=employee_id)

    # 🚫 Extra security: Prevent editing a PDG or another Gérant
    if employee.role in ["pdg", "gerant"]:
        messages.error(request, "You cannot edit a PDG or another Gérant.")
        return redirect("gerant_dashboard:manage_employees")

    if request.method == "POST":
        form = EmployeeEditForm(request.POST, instance=employee)
        if form.is_valid():
            # 🚫 Extra security: Prevent saving a PDG or Gérant role
            if form.cleaned_data["role"] in ["pdg", "gerant"]:
                messages.error(request, "You cannot assign the role of PDG or Gérant.")
                return redirect("gerant_dashboard:manage_employees")

            form.save()
            messages.success(request, "Employee updated successfully!")
            return redirect("gerant_dashboard:manage_employees")

    else:
        form = EmployeeEditForm(instance=employee)

    return render(request, "gerant_dashboard/edit_employee.html", {"form": form, "employee": employee})




















@login_required
def manage_stock(request):
    """View to list stock items for the Gérant's store"""
    store = request.user.store  # Get the Gérant's store
    stock_items = Stock.objects.filter(store=store)  # Fetch stock for this store
    return render(request, "gerant_dashboard/manage_stock.html", {"stock_items": stock_items})


@login_required
def add_stock(request):
    """View to add a new stock item"""
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock_item = form.save(commit=False)
            stock_item.store = request.user.store  # Assign stock to the Gérant's store
            stock_item.save()
            return redirect("gerant_dashboard:manage_stock")
    else:
        form = StockForm()

    return render(request, "gerant_dashboard/stock_form.html", {"form": form})


@login_required
def edit_stock(request, stock_id):
    """View to edit an existing stock item"""
    stock_item = get_object_or_404(Stock, id=stock_id, store=request.user.store)

    if request.method == "POST":
        form = StockForm(request.POST, instance=stock_item)
        if form.is_valid():
            form.save()
            return redirect("gerant_dashboard:manage_stock")
    else:
        form = StockForm(instance=stock_item)

    return render(request, "gerant_dashboard/stock_form.html", {"form": form})


@login_required
def delete_stock(request, stock_id):
    """View to delete a stock item"""
    stock_item = get_object_or_404(Stock, id=stock_id, store=request.user.store)

    if request.method == "POST":
        stock_item.delete()
        return redirect("gerant_dashboard:manage_stock")

    return render(request, "gerant_dashboard/confirm_delete.html", {"stock_item": stock_item})





def list_tables(request):
    tables = Table.objects.filter(store=request.user.store).order_by("number")
    return render(request, 'gerant_dashboard/list_tables.html', {'tables': tables})


def add_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            store = request.user.store
            last_table = Table.objects.filter(store=store).order_by("number").last()
            next_number = last_table.number + 1 if last_table else 1  # Auto-increment

            table = form.save(commit=False)
            table.store = store
            table.number = next_number  # Assign the correct number
            table.save()

            messages.success(request, "Table added successfully!")
            return redirect('gerant_dashboard:list_tables')
    else:
        form = TableForm()
    return render(request, 'gerant_dashboard/add_table.html', {'form': form})


def edit_table(request, table_id):
    table = get_object_or_404(Table, id=table_id, store=request.user.store)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, "Table updated successfully!")
            return redirect('gerant_dashboard:list_tables')
    else:
        form = TableForm(instance=table)
    return render(request, 'gerant_dashboard/edit_table.html', {'form': form, 'table': table})


def delete_table(request, table_id):
    store = request.user.store
    table = get_object_or_404(Table, id=table_id, store=store)
    table.delete()

    # Reorder table numbers to maintain sequence
    tables = Table.objects.filter(store=store).order_by("number")
    for index, table in enumerate(tables, start=1):
        table.number = index  # Reset table numbers
        table.save()

    messages.success(request, "Table deleted and numbers reordered!")
    return redirect('gerant_dashboard:list_tables')







from django.shortcuts import render, get_object_or_404, redirect
from .models import Table, Reservation
from .forms import ReservationForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Table, Reservation
from .forms import ReservationForm


def reservation_list(request):
    tables = Table.objects.prefetch_related("reservations").all()

    return render(request, "gerant_dashboard/reservation_list.html", {
        "tables": tables,
    })


def add_reservation(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.table = table
            reservation.status = "reserved"
            reservation.save()
            return redirect("gerant_dashboard:reservation_list")
    else:
        form = ReservationForm(initial={"table": table})

    return render(request, "gerant_dashboard/add_reservation.html", {"form": form})


def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)  # Get the reservation

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)  # Bind form with existing instance
        if form.is_valid():
            form.save()
            return redirect("gerant_dashboard:reservation_list")
    else:
        form = ReservationForm(instance=reservation)  # Pre-fill with old data

    return render(request, "gerant_dashboard/edit_reservation.html", {"form": form})


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Move to history
    ReservationHistory.objects.create(
        table=reservation.table,
        client_name=reservation.client_name,
        client_contact=reservation.client_contact,
        date=reservation.date,
        time=reservation.time,
        status="cancelled"
    )

    reservation.delete()
    return redirect("gerant_dashboard:reservation_list")


def complete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Move to history
    ReservationHistory.objects.create(
        table=reservation.table,
        client_name=reservation.client_name,
        client_contact=reservation.client_contact,
        date=reservation.date,
        time=reservation.time,
        status="completed"
    )

    reservation.delete()
    return redirect("gerant_dashboard:reservation_list")


def reservation_history(request):
    history = ReservationHistory.objects.all().order_by("-date", "-time")
    return render(request, "gerant_dashboard/reservation_history.html", {"history": history})











from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import SpecialClient
from .forms import SpecialClientForm

User = get_user_model()

def special_client_list(request):
    """ Show only special clients """
    special_clients = SpecialClient.objects.all()
    return render(request, "gerant_dashboard/special_client_list.html", {"special_clients": special_clients})

def add_special_client(request):
    """ Form to add a special client """
    if request.method == "POST":
        form = SpecialClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("gerant_dashboard:special_client_list")
    else:
        form = SpecialClientForm()

    return render(request, "gerant_dashboard/add_special_client.html", {"form": form})

def edit_special_client(request, client_id):
    """ Edit special client type """
    special_client = get_object_or_404(SpecialClient, id=client_id)

    if request.method == "POST":
        form = SpecialClientForm(request.POST, instance=special_client)
        if form.is_valid():
            form.save()
            return redirect("gerant_dashboard:special_client_list")
    else:
        form = SpecialClientForm(instance=special_client)

    return render(request, "gerant_dashboard/edit_special_client.html", {"form": form, "special_client": special_client})

def delete_special_client(request, client_id):
    """ Delete a special client """
    special_client = get_object_or_404(SpecialClient, id=client_id)
    special_client.delete()
    return redirect("gerant_dashboard:special_client_list")



from django.shortcuts import render, get_object_or_404, redirect
from pdg_dashboard.models import Expense
from .forms import ExpenseForm  # We'll create this next
from django.contrib.auth.decorators import login_required

@login_required
def expense_list(request):
    store = request.user.managed_store
    expenses = Expense.objects.filter(store=store).order_by('-created_at')
    return render(request, "gerant_dashboard/expense_list.html", {"expenses": expenses})

@login_required
def add_expense(request):
    store = request.user.managed_store
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.store = store
            expense.save()
            return redirect("gerant_dashboard:expense_list")
    else:
        form = ExpenseForm()
    return render(request, "gerant_dashboard/add_expense.html", {"form": form})

@login_required
def edit_expense(request, expense_id):
    store = request.user.managed_store
    expense = get_object_or_404(Expense, id=expense_id, store=store)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("gerant_dashboard:expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "gerant_dashboard/edit_expense.html", {"form": form, "expense": expense})

@login_required
def delete_expense(request, expense_id):
    store = request.user.managed_store
    expense = get_object_or_404(Expense, id=expense_id, store=store)
    expense.delete()

    # Reorder numbers after deletion
    all_expenses = Expense.objects.filter(store=store).order_by('number')
    for idx, e in enumerate(all_expenses, start=1):
        if e.number != idx:
            e.number = idx
            e.save()

    return redirect("gerant_dashboard:expense_list")


from django.shortcuts import render, redirect
from .models import DailyMenu
from .utils import calculate_ingredient_needs
from datetime import date
from pdg_dashboard.models import Supplier, SupplierIngredientRequest, Ingredient, Store

from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from pdg_dashboard.models import Ingredient, Supplier, SupplierIngredient, SupplierIngredientRequest
from gerant_dashboard.models import DailyMenu
from gerant_dashboard.utils import calculate_ingredient_needs
from django.contrib.auth.decorators import login_required


@login_required
def view_daily_ingredients(request):
    daily_menu = DailyMenu.objects.filter(date=date.today(), store=request.user.managed_store).first()

    if not daily_menu:
        return render(request, "gerant_dashboard/no_menu_today.html")

    # Calcul des besoins en ingrédients
    ingredient_totals = dict(calculate_ingredient_needs(daily_menu))
    ingredient_totals_list = [
        {"ingredient": ingredient, "quantity": quantity}
        for ingredient, quantity in ingredient_totals.items()
    ]

    if request.method == "POST":
        # Traitement des requêtes d'ingrédients envoyées aux fournisseurs
        supplier_ids = request.POST.getlist("supplier_id")
        ingredient_ids = request.POST.getlist("ingredient_id")
        quantities = request.POST.getlist("ingredient_quantity")

        supplier_ingredient_requests = []

        for supplier_id, ingredient_id, quantity in zip(supplier_ids, ingredient_ids, quantities):
            if quantity.strip() == "":
                continue  # ignore empty inputs

            supplier = get_object_or_404(Supplier, id=supplier_id)
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            store = request.user.managed_store

            supplier_ingredient_requests.append(
                SupplierIngredientRequest(
                    supplier=supplier,
                    ingredient=ingredient,
                    store=store,
                    quantity_requested=quantity
                )
            )

        SupplierIngredientRequest.objects.bulk_create(supplier_ingredient_requests)
        return redirect("gerant_dashboard:request_sent_confirmation")

    suppliers = Supplier.objects.all()

    context = {
        "daily_menu": daily_menu,
        "ingredient_totals_list": ingredient_totals_list,
        "suppliers": suppliers,
    }

    return render(request, "gerant_dashboard/ingredient_needs.html", context)


# gerant_dashboard/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from gerant_dashboard.models import DailyMenu, DailyMenuDish
from pdg_dashboard.models import Store

@login_required
def historique_menus(request):
    try:
        store = request.user.managed_store  # related_name from Store.gerant
        menus = DailyMenu.objects.filter(store=store).prefetch_related('dailymenudish_set__dish').order_by('-date')
    except Store.DoesNotExist:
        menus = DailyMenu.objects.none()  # In case the user doesn't manage any store

    return render(request, 'gerant_dashboard/historique_menus.html', {'menus': menus})




from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from gerant_dashboard.models import DailyMenu, DailyMenuDish
from pdg_dashboard.models import Dish
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import DailyMenu, DailyMenuDish, Dish
from django.contrib.auth.decorators import login_required

@login_required
def edit_daily_menu(request):
    today = timezone.now().date()
    store = request.user.managed_store  # Get the store of the gerant

    # Get the existing daily menu or create one if it doesn't exist
    try:
        daily_menu = DailyMenu.objects.get(date=today, store=store)
    except DailyMenu.DoesNotExist:
        # If no menu exists for today, let the gerant know or handle accordingly
        return redirect('gerant_dashboard:historique_menus')  # or create new

    # Fetch all dishes for the store
    dishes = Dish.objects.filter(store=store)

    # Create a dictionary for the existing quantities in the menu
    quantities = {dm_dish.dish_id: dm_dish.quantity for dm_dish in daily_menu.dailymenudish_set.all()}

    # Attach the existing quantity to each dish
    for dish in dishes:
        dish.existing_quantity = quantities.get(dish.id, 0)

    # Handle POST request when the gerant submits the form to update quantities
    if request.method == 'POST':
        for dish in dishes:
            quantity = request.POST.get(f'quantity_{dish.id}')
            if quantity is not None and quantity.strip() != '':
                try:
                    quantity = int(quantity)
                    if quantity > 0:
                        menu_dish, created = DailyMenuDish.objects.get_or_create(
                            daily_menu=daily_menu,
                            dish=dish,
                            defaults={'quantity': quantity}
                        )
                        if not created:
                            menu_dish.quantity = quantity
                            menu_dish.save()
                    else:
                        DailyMenuDish.objects.filter(daily_menu=daily_menu, dish=dish).delete()
                except ValueError:
                    continue

        return redirect('gerant_dashboard:historique_menus')  # Redirect to the historical menu page

    return render(request, 'gerant_dashboard/edit_daily_menu.html', {
        'daily_menu': daily_menu,
        'dishes': dishes,
    })

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierIngredientFormSet
from pdg_dashboard.models import Supplier

def manage_supplier_ingredients(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == 'POST':
        formset = SupplierIngredientFormSet(request.POST, queryset=SupplierIngredient.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    ingredient = form.cleaned_data['ingredient']
                    price = form.cleaned_data['price_per_unit']
                    # On crée l’objet si pas déjà lié
                    SupplierIngredient.objects.get_or_create(
                        supplier=supplier,
                        ingredient=ingredient,
                        defaults={
                            'price_per_unit': price,
                        }
                    )
            return redirect('gerant_dashboard:home')
    else:
        formset = SupplierIngredientFormSet(queryset=SupplierIngredient.objects.none())

    return render(request, 'gerant_dashboard/manage_supplier_ingredients.html', {
        'supplier': supplier,
        'formset': formset,
    })



from django.shortcuts import render

def request_sent_confirmation(request):
    return render(request, 'gerant_dashboard/request_sent_confirmation.html')
