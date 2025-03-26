from django.urls import path
from .views import client_signup

app_name = "authentication"

urlpatterns = [
    path("signup/", client_signup, name="client_signup"),
]
