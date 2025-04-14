from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from pdg_dashboard.models import SupplierIngredientRequest, SupplierResponse
from django.contrib.auth.decorators import login_required

User = get_user_model()  # This ensures you're using 'authentication.User'

def is_fournisseur(user):
    """Check if the user is a Gérant."""
    return user.is_authenticated and user.role == "fournisseur"

@login_required
def fournisseur_dashboard(request):
    """Main dashboard for Gérant, showing store overview."""
    if not is_fournisseur(request.user):
        return redirect("authentication:login")  # Redirect if not Gérant

    store = request.user.store  # Get the store assigned to the Gérant

    context = {
        "store": store,
    }
    return render(request, "fournisseur_dashboard/home.html", context)





@login_required
def view_requests(request):
    supplier = request.user.supplier_profile  # si tu as un profil lié à l'utilisateur
    requests = SupplierIngredientRequest.objects.filter(supplier=supplier, supplierresponse__isnull=True)
    return render(request, 'fournisseur_dashboard/requests.html', {'requests': requests})

@login_required
def respond_to_request(request, request_id):
    req = get_object_or_404(SupplierIngredientRequest, id=request_id)

    if request.method == 'POST':
        accepted = request.POST.get('accepted') == 'yes'
        comment = request.POST.get('comment', '')

        SupplierResponse.objects.create(
            request=req,
            accepted=accepted,
            comment=comment
        )

        return redirect('fournisseur_dashboard:view_requests')

    return render(request, 'fournisseur_dashboard/respond.html', {'req': req})
