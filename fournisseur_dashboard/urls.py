from django.urls import path
from . import views

app_name = 'fournisseur_dashboard'

urlpatterns = [
    path('home/', views.fournisseur_dashboard, name='home'),

    path('demandes/', views.view_requests, name='view_requests'),
    path('repondre/<int:request_id>/', views.respond_to_request, name='respond_to_request'),
]
