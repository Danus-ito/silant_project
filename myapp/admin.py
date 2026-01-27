from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import Reference, Machine, Maintenance, Complaint

# Кастомизация групп в админке
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_user_count']
    search_fields = ['name']
    
    def get_user_count(self, obj):
        return obj.user_set.count()
    get_user_count.short_description = 'Количество пользователей'

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Кастомизация пользователей
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_groups', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Группы'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Справочники
@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ['get_type_display', 'get_name', 'get_description_short']
    list_filter = ['type']
    search_fields = ['name', 'description']
    ordering = ['type', 'name']
    
    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Название'
    
    def get_description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    get_description_short.short_description = 'Описание'

# Машины
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ['factory_number', 'get_tech_model', 'get_client', 'get_service_company', 'shipment_date']
    list_filter = ['tech_model', 'engine_model', 'client', 'service_company', 'shipment_date']
    search_fields = ['factory_number', 'engine_number', 'transmission_number', 'supply_contract']
    raw_id_fields = ['client', 'service_company']
    date_hierarchy = 'shipment_date'
    
    def get_tech_model(self, obj):
        return obj.tech_model.name
    get_tech_model.short_description = 'Модель техники'
    
    def get_client(self, obj):
        return obj.client.username
    get_client.short_description = 'Клиент'
    
    def get_service_company(self, obj):
        return obj.service_company.username
    get_service_company.short_description = 'Сервисная компания'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('factory_number', 'tech_model', 'engine_model', 'engine_number')
        }),
        ('Трансмиссия и мосты', {
            'fields': ('transmission_model', 'transmission_number',
                      'drive_axle_model', 'drive_axle_number',
                      'steerable_axle_model', 'steerable_axle_number')
        }),
        ('Поставка', {
            'fields': ('supply_contract', 'shipment_date', 'consignee', 
                      'delivery_address', 'equipment')
        }),
        ('Владельцы', {
            'fields': ('client', 'service_company')
        }),
    )

# ТО
@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['get_machine', 'get_type', 'date', 'operating_time', 'get_service_company']
    list_filter = ['type', 'date', 'service_company']
    search_fields = ['work_order_number', 'machine__factory_number']
    raw_id_fields = ['machine', 'service_company']
    date_hierarchy = 'date'
    
    def get_machine(self, obj):
        return obj.machine.factory_number
    get_machine.short_description = 'Машина'
    
    def get_type(self, obj):
        return obj.type.name
    get_type.short_description = 'Вид ТО'
    
    def get_service_company(self, obj):
        return obj.service_company.username
    get_service_company.short_description = 'Сервисная компания'

# Рекламации
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['get_machine', 'failure_date', 'get_failure_node', 'recovery_date', 'downtime']
    list_filter = ['failure_node', 'recovery_method', 'service_company', 'failure_date']
    search_fields = ['machine__factory_number', 'failure_description', 'spare_parts']
    raw_id_fields = ['machine', 'service_company']
    date_hierarchy = 'failure_date'
    readonly_fields = ['downtime']
    
    def get_machine(self, obj):
        return obj.machine.factory_number
    get_machine.short_description = 'Машина'
    
    def get_failure_node(self, obj):
        return obj.failure_node.name
    get_failure_node.short_description = 'Узел отказа'