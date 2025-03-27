from django.urls import path
from .views import login_view, logout_view, client_signup

app_name = "authentication"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", client_signup, name="signup"),
]
