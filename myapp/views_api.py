from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Machine, Maintenance, Complaint, Reference
from .serializers import (
    MachineSerializer, MaintenanceSerializer, ComplaintSerializer,
    ReferenceSerializer, UserSerializer
)

# Класс для получения токена (нужен для urls_api.py)
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key, 
            'user_id': token.user_id,
            'username': token.user.username
        })

# ViewSets для API
class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tech_model', 'engine_model', 'transmission_model', 
                       'drive_axle_model', 'steerable_axle_model',
                       'client', 'service_company']
    search_fields = ['factory_number', 'engine_number', 'transmission_number']
    ordering_fields = ['factory_number', 'shipment_date']
    ordering = ['-shipment_date']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='manager').exists():
            return Machine.objects.all()
        elif user.groups.filter(name='client').exists():
            return Machine.objects.filter(client=user)
        elif user.groups.filter(name='service_company').exists():
            return Machine.objects.filter(service_company=user)
        return Machine.objects.none()

class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'service_company', 'machine']
    search_fields = ['work_order_number', 'machine__factory_number']
    ordering_fields = ['date', 'operating_time']
    ordering = ['-date']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='manager').exists():
            return Maintenance.objects.all()
        elif user.groups.filter(name='client').exists():
            user_machines = Machine.objects.filter(client=user)
            return Maintenance.objects.filter(machine__in=user_machines)
        elif user.groups.filter(name='service_company').exists():
            return Maintenance.objects.filter(service_company=user)
        return Maintenance.objects.none()

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['failure_node', 'recovery_method', 'service_company', 'machine']
    search_fields = ['failure_description', 'spare_parts', 'machine__factory_number']
    ordering_fields = ['failure_date', 'recovery_date', 'downtime']
    ordering = ['-failure_date']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.groups.filter(name='manager').exists():
            return Complaint.objects.all()
        elif user.groups.filter(name='client').exists():
            user_machines = Machine.objects.filter(client=user)
            return Complaint.objects.filter(machine__in=user_machines)
        elif user.groups.filter(name='service_company').exists():
            return Complaint.objects.filter(service_company=user)
        return Complaint.objects.none()

class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# Функция для получения токена (альтернативный вариант)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_auth_token(request):
    """Альтернативная функция для получения токена"""
    from rest_framework.authtoken.models import Token
    from django.contrib.auth.models import User
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Требуется username и password'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            return Response({'error': 'Неверный пароль'}, 
                           status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Пользователь не найден'}, 
                       status=status.HTTP_404_NOT_FOUND)