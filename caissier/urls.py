from django.urls import path
from . import views

app_name = "caissier"

urlpatterns = [

    path('', views.caissier_home, name="home"),
    path('orders/served/', views.served_orders, name="served_orders"),
    path('orders/<int:order_id>/', views.order_detail, name="order_detail"),
    path('orders/<int:order_id>/done/', views.mark_order_done, name="mark_order_done"),
]
