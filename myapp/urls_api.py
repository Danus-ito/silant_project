from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r'machines', views_api.MachineViewSet, basename='machine')
router.register(r'maintenances', views_api.MaintenanceViewSet, basename='maintenance')
router.register(r'complaints', views_api.ComplaintViewSet, basename='complaint')
router.register(r'references', views_api.ReferenceViewSet, basename='reference')

urlpatterns = [
    path('get-token/', views_api.CustomObtainAuthToken.as_view(), name='api_token_auth'),
    path('', include(router.urls)),
]