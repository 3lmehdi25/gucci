from django.urls import path

from . import views
from .views import chef_dashboard ,declare_daily_menu
app_name = "chef_dashboard"

urlpatterns = [
    path("", chef_dashboard, name="home"),  # chef/ will load this view
    path('declare-menu/', views.declare_daily_menu, name='declare_daily_menu'),
    path("orders/", views.chef_orders_view, name="chef_orders_view"),
    path("orders/<int:order_id>/update/", views.chef_update_order_status, name="chef_update_order_status"),

]
