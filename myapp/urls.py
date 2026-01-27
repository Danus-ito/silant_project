from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('machine/<int:pk>/', views.machine_detail, name='machine_detail'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
]