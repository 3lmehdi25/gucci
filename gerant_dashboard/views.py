from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pdg_dashboard.models import Store
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import User
from pdg_dashboard.models import Store
from .forms import  EmployeeEditForm, EmployeeCreateForm


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