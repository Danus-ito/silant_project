# myapp/filters.py
import django_filters
from .models import Machine, Maintenance, Complaint

class MachineFilter(django_filters.FilterSet):
    """Фильтр для машин"""
    factory_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Заводской номер'
    )
    
    tech_model = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Модель техники'
    )
    
    class Meta:
        model = Machine
        fields = ['factory_number', 'tech_model', 'client', 'service_company']

class MaintenanceFilter(django_filters.FilterSet):
    """Фильтр для ТО"""
    work_order_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Номер заказ-наряда'
    )
    
    class Meta:
        model = Maintenance
        fields = ['type', 'machine', 'service_company']

class ComplaintFilter(django_filters.FilterSet):
    """Фильтр для рекламаций"""
    failure_node = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Узел отказа'
    )
    
    class Meta:
        model = Complaint
        fields = ['failure_node', 'machine', 'service_company']