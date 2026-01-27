from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Machine, Maintenance, Complaint, Reference
from .forms import (
    GuestSearchForm, MachineFilterForm, 
    MaintenanceFilterForm, ComplaintFilterForm
)

def welcome_page(request):
    form = GuestSearchForm(request.GET or None)
    machine = None
    error = None
    
    if request.method == 'GET' and 'factory_number' in request.GET:
        if form.is_valid():
            factory_number = form.cleaned_data['factory_number']
            try:
                machine = Machine.objects.get(factory_number=factory_number)
            except Machine.DoesNotExist:
                error = "Данных о машине с таким заводским номером нет в системе"
    
    return render(request, 'welcome.html', {
        'form': form,
        'machine': machine,
        'error': error,
    })

@login_required
def dashboard(request):
    user = request.user
    
    # Определяем доступные данные по ролям
    if user.groups.filter(name='manager').exists():
        machines_qs = Machine.objects.all()
        maintenances_qs = Maintenance.objects.all()
        complaints_qs = Complaint.objects.all()
        user_role = 'менеджер'
    elif user.groups.filter(name='client').exists():
        machines_qs = Machine.objects.filter(client=user)
        machine_ids = machines_qs.values_list('id', flat=True)
        maintenances_qs = Maintenance.objects.filter(machine_id__in=machine_ids)
        complaints_qs = Complaint.objects.filter(machine_id__in=machine_ids)
        user_role = 'клиент'
    elif user.groups.filter(name='service_company').exists():
        machines_qs = Machine.objects.filter(service_company=user)
        maintenances_qs = Maintenance.objects.filter(service_company=user)
        complaints_qs = Complaint.objects.filter(service_company=user)
        user_role = 'сервисная компания'
    else:
        machines_qs = Machine.objects.none()
        maintenances_qs = Maintenance.objects.none()
        complaints_qs = Complaint.objects.none()
        user_role = 'гость'
    
    # ИНИЦИАЛИЗАЦИЯ ФОРМ
    machine_filter_form = MachineFilterForm(request.GET)
    maintenance_filter_form = MaintenanceFilterForm(request.GET)
    complaint_filter_form = ComplaintFilterForm(request.GET)
    
    # ФИЛЬТРАЦИЯ МАШИН (работает через Django форму)
    if machine_filter_form.is_valid():
        data = machine_filter_form.cleaned_data
        
        if data.get('factory_number'):
            machines_qs = machines_qs.filter(factory_number__icontains=data['factory_number'])
        if data.get('tech_model'):
            machines_qs = machines_qs.filter(tech_model=data['tech_model'])
        if data.get('engine_model'):
            machines_qs = machines_qs.filter(engine_model=data['engine_model'])
        if data.get('transmission_model'):
            machines_qs = machines_qs.filter(transmission_model=data['transmission_model'])
        if data.get('client'):
            machines_qs = machines_qs.filter(client=data['client'])
        if data.get('service_company'):
            machines_qs = machines_qs.filter(service_company=data['service_company'])
        if data.get('shipment_date_from'):
            machines_qs = machines_qs.filter(shipment_date__gte=data['shipment_date_from'])
        if data.get('shipment_date_to'):
            machines_qs = machines_qs.filter(shipment_date__lte=data['shipment_date_to'])
    
    # ФИЛЬТРАЦИЯ ТО
    if maintenance_filter_form.is_valid():
        data = maintenance_filter_form.cleaned_data
        
        if data.get('type'):
            maintenances_qs = maintenances_qs.filter(type=data['type'])
        if data.get('machine__factory_number'):
            maintenances_qs = maintenances_qs.filter(
                machine__factory_number__icontains=data['machine__factory_number']
            )
        if data.get('service_company'):
            maintenances_qs = maintenances_qs.filter(service_company=data['service_company'])
        if data.get('date_from'):
            maintenances_qs = maintenances_qs.filter(date__gte=data['date_from'])
        if data.get('date_to'):
            maintenances_qs = maintenances_qs.filter(date__lte=data['date_to'])
    
    # ФИЛЬТРАЦИЯ РЕКЛАМАЦИЙ
    if complaint_filter_form.is_valid():
        data = complaint_filter_form.cleaned_data
        
        if data.get('failure_node'):
            complaints_qs = complaints_qs.filter(failure_node=data['failure_node'])
        if data.get('recovery_method'):
            complaints_qs = complaints_qs.filter(recovery_method=data['recovery_method'])
        if data.get('machine__factory_number'):
            complaints_qs = complaints_qs.filter(
                machine__factory_number__icontains=data['machine__factory_number']
            )
        if data.get('service_company'):
            complaints_qs = complaints_qs.filter(service_company=data['service_company'])
        if data.get('failure_date_from'):
            complaints_qs = complaints_qs.filter(failure_date__gte=data['failure_date_from'])
        if data.get('failure_date_to'):
            complaints_qs = complaints_qs.filter(failure_date__lte=data['failure_date_to'])
    
    # СОРТИРОВКА
    sort_field = request.GET.get('sort', '')
    sort_order = request.GET.get('order', 'asc')
    
    if sort_field.startswith('machine_'):
        field_name = sort_field.replace('machine_', '')
        if field_name in ['factory_number', 'shipment_date']:
            if sort_order == 'desc':
                machines_qs = machines_qs.order_by(f'-{field_name}')
            else:
                machines_qs = machines_qs.order_by(field_name)
    elif sort_field.startswith('maintenance_'):
        field_name = sort_field.replace('maintenance_', '')
        if field_name in ['date', 'operating_time']:
            if sort_order == 'desc':
                maintenances_qs = maintenances_qs.order_by(f'-{field_name}')
            else:
                maintenances_qs = maintenances_qs.order_by(field_name)
    elif sort_field.startswith('complaint_'):
        field_name = sort_field.replace('complaint_', '')
        if field_name in ['failure_date', 'recovery_date', 'downtime']:
            if sort_order == 'desc':
                complaints_qs = complaints_qs.order_by(f'-{field_name}')
            else:
                complaints_qs = complaints_qs.order_by(field_name)
    
    # ПАГИНАЦИЯ
    page = request.GET.get('page', 1)
    paginator_machines = Paginator(machines_qs, 10)
    paginator_maintenances = Paginator(maintenances_qs, 10)
    paginator_complaints = Paginator(complaints_qs, 10)
    
    return render(request, 'dashboard.html', {
        'user': user,
        'user_role': user_role,
        'machines': paginator_machines.get_page(page),
        'maintenances': paginator_maintenances.get_page(page),
        'complaints': paginator_complaints.get_page(page),
        'machine_count': machines_qs.count(),
        'maintenance_count': maintenances_qs.count(),
        'complaint_count': complaints_qs.count(),
        'machine_filter_form': machine_filter_form,
        'maintenance_filter_form': maintenance_filter_form,
        'complaint_filter_form': complaint_filter_form,
        'current_sort': sort_field,
        'current_order': sort_order,
        'page': page,
    })

@login_required
def machine_detail(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    user = request.user
    
    has_access = False
    if user.groups.filter(name='manager').exists():
        has_access = True
    elif user.groups.filter(name='client').exists() and machine.client == user:
        has_access = True
    elif user.groups.filter(name='service_company').exists() and machine.service_company == user:
        has_access = True
    
    if not has_access:
        return redirect('dashboard')
    
    return render(request, 'machine_detail.html', {
        'machine': machine,
        'maintenances': Maintenance.objects.filter(machine=machine).order_by('-date')[:5],
        'complaints': Complaint.objects.filter(machine=machine).order_by('-failure_date')[:5],
        'user': user,
    })

@login_required
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    user = request.user
    
    has_access = False
    if user.groups.filter(name='manager').exists():
        has_access = True
    elif user.groups.filter(name='client').exists() and maintenance.machine.client == user:
        has_access = True
    elif user.groups.filter(name='service_company').exists() and maintenance.service_company == user:
        has_access = True
    
    if not has_access:
        return redirect('dashboard')
    
    return render(request, 'maintenance_detail.html', {
        'maintenance': maintenance,
        'user': user,
    })

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    user = request.user
    
    has_access = False
    if user.groups.filter(name='manager').exists():
        has_access = True
    elif user.groups.filter(name='client').exists() and complaint.machine.client == user:
        has_access = True
    elif user.groups.filter(name='service_company').exists() and complaint.service_company == user:
        has_access = True
    
    if not has_access:
        return redirect('dashboard')
    
    return render(request, 'complaint_detail.html', {
        'complaint': complaint,
        'user': user,
    })