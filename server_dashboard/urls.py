# serveur_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'server_dashboard'

urlpatterns = [
    path('pending_orders/', views.pending_orders, name='pending_orders'),
    path('mark_as_served/<int:order_id>/', views.mark_as_served, name='mark_as_served'),
    path('assigned_tables/', views.assigned_tables, name='assigned_tables'),
]
