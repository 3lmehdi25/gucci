# server/urls.py

from django.urls import path
from . import views

# Add app_name to define the namespace for this app
app_name = 'server'

urlpatterns = [
    path('home/', views.server_dashboard, name='home'),  # Name for the server home page

]
