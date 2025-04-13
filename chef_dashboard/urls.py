from django.urls import path
from .views import chef_dashboard  # or any view you want to show

app_name = "chef_dashboard"

urlpatterns = [
    path("", chef_dashboard, name="home"),  # chef/ will load this view
]
