from django import forms
from django.contrib.auth.models import User
from .models import Machine, Maintenance, Complaint, Reference

# Форма поиска для гостей
class GuestSearchForm(forms.Form):
    factory_number = forms.CharField(
        label='Заводской номер машины',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заводской номер...',
            'autofocus': True
        })
    )

# Фильтры для машин
class MachineFilterForm(forms.Form):
    factory_number = forms.CharField(
        label='Заводской номер',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по номеру...'})
    )
    
    tech_model = forms.ModelChoiceField(
        label='Модель техники',
        queryset=Reference.objects.filter(type='tech_model'),
        required=False,
        empty_label='Все модели',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    engine_model = forms.ModelChoiceField(
        label='Модель двигателя',
        queryset=Reference.objects.filter(type='engine_model'),
        required=False,
        empty_label='Все двигатели',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    transmission_model = forms.ModelChoiceField(
        label='Модель трансмиссии',
        queryset=Reference.objects.filter(type='transmission_model'),
        required=False,
        empty_label='Все трансмиссии',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    client = forms.ModelChoiceField(
        label='Клиент',
        queryset=User.objects.filter(groups__name='client'),
        required=False,
        empty_label='Все клиенты',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    service_company = forms.ModelChoiceField(
        label='Сервисная компания',
        queryset=User.objects.filter(groups__name='service_company'),
        required=False,
        empty_label='Все компании',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    shipment_date_from = forms.DateField(
        label='Дата отгрузки с',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    shipment_date_to = forms.DateField(
        label='по',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

# Фильтры для ТО
class MaintenanceFilterForm(forms.Form):
    type = forms.ModelChoiceField(
        label='Вид ТО',
        queryset=Reference.objects.filter(type='maintenance_type'),
        required=False,
        empty_label='Все виды ТО',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    machine__factory_number = forms.CharField(
        label='Заводской номер машины',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фильтр по машине...'})
    )
    
    service_company = forms.ModelChoiceField(
        label='Сервисная компания',
        queryset=User.objects.filter(groups__name='service_company'),
        required=False,
        empty_label='Все компании',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        label='Дата ТО с',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    date_to = forms.DateField(
        label='по',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

# Фильтры для рекламаций
class ComplaintFilterForm(forms.Form):
    failure_node = forms.ModelChoiceField(
        label='Узел отказа',
        queryset=Reference.objects.filter(type='failure_node'),
        required=False,
        empty_label='Все узлы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    recovery_method = forms.ModelChoiceField(
        label='Способ восстановления',
        queryset=Reference.objects.filter(type='recovery_method'),
        required=False,
        empty_label='Все способы',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    machine__factory_number = forms.CharField(
        label='Заводской номер машины',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фильтр по машине...'})
    )
    
    service_company = forms.ModelChoiceField(
        label='Сервисная компания',
        queryset=User.objects.filter(groups__name='service_company'),
        required=False,
        empty_label='Все компании',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    failure_date_from = forms.DateField(
        label='Дата отказа с',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    failure_date_to = forms.DateField(
        label='по',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

# Быстрый поиск
class QuickSearchForm(forms.Form):
    search = forms.CharField(
        label='Быстрый поиск',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Номер, модель, узел...'
        })
    )