from rest_framework import serializers
from .models import Machine, Maintenance, Complaint, Reference
from django.contrib.auth.models import User

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class MachineSerializer(serializers.ModelSerializer):
    tech_model_name = serializers.CharField(source='tech_model.name', read_only=True)
    client_username = serializers.CharField(source='client.username', read_only=True)
    service_company_username = serializers.CharField(source='service_company.username', read_only=True)
    
    class Meta:
        model = Machine
        fields = '__all__'
        extra_fields = ['tech_model_name', 'client_username', 'service_company_username']

class MaintenanceSerializer(serializers.ModelSerializer):
    machine_factory_number = serializers.CharField(source='machine.factory_number', read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    
    class Meta:
        model = Maintenance
        fields = '__all__'
        extra_fields = ['machine_factory_number', 'type_name']

class ComplaintSerializer(serializers.ModelSerializer):
    machine_factory_number = serializers.CharField(source='machine.factory_number', read_only=True)
    failure_node_name = serializers.CharField(source='failure_node.name', read_only=True)
    recovery_method_name = serializers.CharField(source='recovery_method.name', read_only=True)
    
    class Meta:
        model = Complaint
        fields = '__all__'
        extra_fields = ['machine_factory_number', 'failure_node_name', 'recovery_method_name']