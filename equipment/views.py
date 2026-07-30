from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import Equipment, EquipmentAuditLog
from .forms import EquipmentForm
from django.db import models


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_list(request):
    equipment_qs = Equipment.objects.select_related('category', 'brand', 'vendor').all()

    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    if search_query:
        equipment_qs = equipment_qs.filter(
            models.Q(equipment_name__icontains=search_query) |
            models.Q(equipment_code__icontains=search_query) |
            models.Q(serial_number__icontains=search_query)
        )

    if status_filter:
        equipment_qs = equipment_qs.filter(current_status=status_filter)

    context = {
        'equipment_list': equipment_qs,
        'search_query': search_query,
        'status_filter': status_filter,
        'status_choices': Equipment.Status.choices,
    }
    return render(request, 'equipment/equipment_list.html', context)

@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_add(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment added successfully.')
            return redirect('equipment:equipment_list')
    else:
        form = EquipmentForm()
    return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'Add Equipment'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_edit(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Equipment updated successfully.')
            return redirect('equipment:equipment_list')
    else:
        form = EquipmentForm(instance=equipment)
    return render(request, 'equipment/equipment_form.html', {'form': form, 'title': 'Edit Equipment'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_delete(request, pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    if request.method == 'POST':
        equipment.delete()
        messages.success(request, 'Equipment deleted successfully.')
        return redirect('equipment:equipment_list')
    return render(request, 'equipment/equipment_confirm_delete.html', {'equipment': equipment})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def audit_log_list(request):
    logs = EquipmentAuditLog.objects.select_related('equipment', 'performed_by').all()
    return render(request, 'equipment/audit_log_list.html', {'logs': logs})