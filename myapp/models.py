from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Reference(models.Model):
    TYPE_CHOICES = [
        ('tech_model', 'Модель техники'),
        ('engine_model', 'Модель двигателя'),
        ('transmission_model', 'Модель трансмиссии'),
        ('drive_axle_model', 'Модель ведущего моста'),
        ('steerable_axle_model', 'Модель управляемого моста'),
        ('maintenance_type', 'Вид ТО'),
        ('failure_node', 'Узел отказа'),
        ('recovery_method', 'Способ восстановления'),
        ('service_company_ref', 'Сервисная компания (справочник)'),
    ]
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Тип справочника")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    
    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        unique_together = ['type', 'name']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"

class Machine(models.Model):
    factory_number = models.CharField(max_length=50, unique=True, verbose_name="Зав. № машины")
    
    # Справочники с уникальными related_name
    tech_model = models.ForeignKey(Reference, on_delete=models.PROTECT, 
                                   limit_choices_to={'type': 'tech_model'},
                                   related_name='tech_model_machines',
                                   verbose_name="Модель техники")
    engine_model = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                     limit_choices_to={'type': 'engine_model'},
                                     related_name='engine_model_machines',
                                     verbose_name="Модель двигателя")
    engine_number = models.CharField(max_length=50, verbose_name="Зав. № двигателя")
    
    transmission_model = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                          limit_choices_to={'type': 'transmission_model'},
                                          related_name='transmission_model_machines',
                                          verbose_name="Модель трансмиссии")
    transmission_number = models.CharField(max_length=50, verbose_name="Зав. № трансмиссии")
    
    drive_axle_model = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                        limit_choices_to={'type': 'drive_axle_model'},
                                        related_name='drive_axle_model_machines',
                                        verbose_name="Модель ведущего моста")
    drive_axle_number = models.CharField(max_length=50, verbose_name="Зав. № ведущего моста")
    
    steerable_axle_model = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                            limit_choices_to={'type': 'steerable_axle_model'},
                                            related_name='steerable_axle_model_machines',
                                            verbose_name="Модель управляемого моста")
    steerable_axle_number = models.CharField(max_length=50, verbose_name="Зав. № управляемого моста")
    
    # Остальные поля
    supply_contract = models.CharField(max_length=200, verbose_name="Договор поставки №, дата")
    shipment_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=200, verbose_name="Грузополучатель")
    delivery_address = models.TextField(verbose_name="Адрес поставки")
    equipment = models.TextField(verbose_name="Комплектация", blank=True)
    
    # Связи с пользователями
    client = models.ForeignKey(User, on_delete=models.PROTECT, 
                               related_name='client_machines',
                               limit_choices_to={'groups__name': 'client'},
                               verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                       related_name='service_machines',
                                       limit_choices_to={'groups__name': 'service_company'},
                                       verbose_name="Сервисная компания")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['-shipment_date']
    
    def __str__(self):
        return f"{self.tech_model.name} №{self.factory_number}"

class Maintenance(models.Model):
    type = models.ForeignKey(Reference, on_delete=models.PROTECT,
                            limit_choices_to={'type': 'maintenance_type'},
                            related_name='maintenance_type_records',
                            verbose_name="Вид ТО")
    date = models.DateField(verbose_name="Дата проведения ТО")
    operating_time = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    work_order_number = models.CharField(max_length=50, verbose_name="№ заказ-наряда")
    work_order_date = models.DateField(verbose_name="Дата заказ-наряда")
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                       limit_choices_to={'groups__name': 'service_company'},
                                       verbose_name="Сервисная компания")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Техническое обслуживание"
        ordering = ['-date']
    
    def __str__(self):
        return f"ТО {self.machine} от {self.date}"

class Complaint(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_time = models.PositiveIntegerField(verbose_name="Наработка, м/час")
    
    failure_node = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                    limit_choices_to={'type': 'failure_node'},
                                    related_name='failure_node_complaints',
                                    verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    
    recovery_method = models.ForeignKey(Reference, on_delete=models.PROTECT,
                                       limit_choices_to={'type': 'recovery_method'},
                                       related_name='recovery_method_complaints',
                                       verbose_name="Способ восстановления")
    spare_parts = models.TextField(verbose_name="Используемые запасные части", blank=True)
    recovery_date = models.DateField(verbose_name="Дата восстановления")
    
    downtime = models.PositiveIntegerField(verbose_name="Время простоя техники", editable=False)
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT,
                                       limit_choices_to={'groups__name': 'service_company'},
                                       verbose_name="Сервисная компания")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-failure_date']
    
    def save(self, *args, **kwargs):
        self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Рекламация {self.machine} от {self.failure_date}"

# Сигнал для создания групп
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    groups = ['manager', 'client', 'service_company']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    print("✅ Группы пользователей созданы")