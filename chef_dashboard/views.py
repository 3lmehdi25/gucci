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



from pdg_dashboard.models import Dish
from chef_dashboard.forms import DailyMenuForm

@login_required
def declare_daily_menu(request):
    dishes = Dish.objects.all()

    if request.method == 'POST':
        form = DailyMenuForm(request.POST)
        if form.is_valid():
            daily_menu = form.save(commit=False)
            daily_menu.created_by = request.user
            daily_menu.save()

            for dish in dishes:
                checkbox = request.POST.get(f'dish_{dish.id}')
                quantity = request.POST.get(f'quantity_{dish.id}')

                if checkbox and quantity:
                    try:
                        quantity = int(quantity)
                        if quantity > 0:
                            from gerant_dashboard.models import DailyMenuDish
                            DailyMenuDish.objects.create(
                                daily_menu=daily_menu,
                                dish=dish,
                                quantity=quantity
                            )
                    except ValueError:
                        continue

            return redirect('chef_dashboard:home')
    else:
        form = DailyMenuForm()

    return render(request, 'chef_dashboard/declare_daily_menu.html', {
        'form': form,
        'dishes': dishes
    })

