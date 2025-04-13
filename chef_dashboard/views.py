from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

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
