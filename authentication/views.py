from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class ClientSignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

def client_signup(request):
    if request.method == "POST":
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "client"  # Ensure client role is set
            user.save()
            login(request, user)
            return redirect("public:home")  # Redirect after signup
    else:
        form = ClientSignupForm()
    return render(request, "authentication/client_signup.html", {"form": form})
