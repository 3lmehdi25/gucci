from django.urls import path
from . import views  # Ajoute cette ligne
from .views import gerant_dashboard, manage_employees, add_employee, \
    delete_employee, edit_employee, manage_stock, add_stock, edit_stock, \
    delete_stock, \
    add_table, list_tables, edit_table, delete_table, \
    edit_reservation, reservation_list, cancel_reservation, \
    add_reservation, complete_reservation, reservation_history, \
    special_client_list, add_special_client, \
    edit_special_client, delete_special_client, expense_list, add_expense, \
    edit_expense, delete_expense  # Only include the home view for now

app_name = "gerant_dashboard"

urlpatterns = [
    path("", gerant_dashboard, name="home"),  # ✅ This is the main dashboard URL
    path("employees/", manage_employees, name="manage_employees"),
    path("employees/add/", add_employee, name="add_employee"),
    path("employees/delete/<int:employee_id>/", delete_employee, name="delete_employee"),
    path("employees/edit/<int:employee_id>/", edit_employee, name="edit_employee"),

    path("manage_stock/", manage_stock, name="manage_stock"),
    path("manage_stock/add/", add_stock, name="add_stock"),
    path("manage_stock/edit/<int:stock_id>/", edit_stock, name="edit_stock"),
    path("manage_stock/delete/<int:stock_id>/", delete_stock, name="delete_stock"),
    path('tables/edit/<int:table_id>/', edit_table, name='edit_table'),
    path('tables/delete/<int:table_id>/', delete_table, name='delete_table'),


    path("tables/", list_tables, name="list_tables"),
    path("tables/add/", add_table, name="add_table"),

    path("reservations/", reservation_list, name="reservation_list"),
    path("reservations/add/<int:table_id>/", add_reservation, name="add_reservation"),
    path("reservations/edit/<int:reservation_id>/", edit_reservation, name="edit_reservation"),
    path("reservations/cancel/<int:reservation_id>/", cancel_reservation, name="cancel_reservation"),
    path("reservations/done/<int:reservation_id>/", complete_reservation, name="complete_reservation"),
    path("reservations/history/", reservation_history, name="reservation_history"),

    path("clients/special/", special_client_list, name="special_client_list"),
    path("clients/special/add/", add_special_client, name="add_special_client"),
    path("clients/special/edit/<int:client_id>/", edit_special_client, name="edit_special_client"),
    path("clients/special/delete/<int:client_id>/", delete_special_client, name="delete_special_client"),

    path('expenses/', expense_list, name='expense_list'),
    path('expenses/add/', add_expense, name='add_expense'),
    path('expenses/edit/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('expenses/delete/<int:expense_id>/', delete_expense, name='delete_expense'),

    path('ingredients-du-jour/', views.view_daily_ingredients, name='daily_ingredients'),
    path('historique-menus/', views.historique_menus, name='historique_menus'),
    path('edit_daily_menu/', views.edit_daily_menu, name='edit_daily_menu'),
    path('manage_supplier_ingredients/<int:supplier_id>/', views.manage_supplier_ingredients, name='manage_supplier_ingredients'),
    path('request-sent-confirmation/', views.request_sent_confirmation, name='request_sent_confirmation'),
]

