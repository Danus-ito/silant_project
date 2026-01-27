# myapp/tables.py
import django_tables2 as tables
from .models import Machine, Maintenance, Complaint

class MachineTable(tables.Table):
    """Таблица машин"""
    factory_number = tables.Column(
        linkify=lambda record: record.get_absolute_url(),
        verbose_name='Зав. №'
    )
    
    class Meta:
        model = Machine
        template_name = "django_tables2/bootstrap4.html"
        fields = (
            'factory_number',
            'tech_model', 
            'engine_model',
            'shipment_date',
            'client',
            'service_company'
        )
        attrs = {
            'class': 'table table-hover table-striped',
            'thead': {'class': 'thead-dark'}
        }

class MaintenanceTable(tables.Table):
    """Таблица ТО"""
    class Meta:
        model = Maintenance
        template_name = "django_tables2/bootstrap4.html"
        fields = ('type', 'date', 'operating_time', 'machine', 'service_company')
        attrs = {'class': 'table table-hover table-striped'}

class ComplaintTable(tables.Table):
    """Таблица рекламаций"""
    class Meta:
        model = Complaint
        template_name = "django_tables2/bootstrap4.html"
        fields = ('failure_date', 'failure_node', 'machine', 'downtime', 'service_company')
        attrs = {'class': 'table table-hover table-striped'}