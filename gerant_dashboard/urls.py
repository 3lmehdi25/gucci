from django.urls import path
from .views import gerant_dashboard, manage_employees, add_employee, \
    delete_employee, edit_employee  # Only include the home view for now

app_name = "gerant_dashboard"

urlpatterns = [
    path("", gerant_dashboard, name="home"),  # ✅ This is the main dashboard URL
  path("employees/", manage_employees, name="manage_employees"),
    path("employees/add/", add_employee, name="add_employee"),
    path("employees/delete/<int:employee_id>/", delete_employee, name="delete_employee"),
    path("employees/edit/<int:employee_id>/", edit_employee, name="edit_employee"),
]

