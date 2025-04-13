# server/urls.py

from django.urls import path
from . import views

# Add app_name to define the namespace for this app
app_name = 'server'

urlpatterns = [

    path("order/new/", views.create_order, name="create_order"),
    path('orders/', views.server_dashboard, name='orders_list'),
    path('order/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order/create/', views.create_order, name='create_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
]
