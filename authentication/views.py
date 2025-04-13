from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# 🔹 Client Signup Form (Username, Email, Password)
class ClientSignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# 🔹 Client Registration View
def client_signup(request):
    if request.method == "POST":
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "client"  # Ensure the role is "client"
            user.save()
            login(request, user)
            return redirect("public:home")  # Redirect to home after signup
    else:
        form = ClientSignupForm()
    return render(request, "authentication/signup.html", {"form": form})

# 🔹 Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect_dashboard(user)  # Redirect based on role
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "authentication/login.html")

# 🔹 Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect("authentication:login")

# 🔹 Redirect Users to Their Dashboards After Login
def redirect_dashboard(user):
    if user.role == "pdg":
        return redirect("pdg_dashboard:home")
    elif user.role == "gerant":
        return redirect("gerant_dashboard:home")
    elif user.role == "chef":
        return redirect("chef_dashboard:home")
    return redirect("public:home")  # Default for other users
