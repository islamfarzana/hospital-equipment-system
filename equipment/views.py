from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import Equipment, EquipmentAuditLog
from .forms import EquipmentForm


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_list(request):
    equipment_qs = Equipment.objects.select_related('category', 'brand', 'vendor').all()
    return render(request, 'equipment/equipment_list.html', {'equipment_list': equipment_qs})


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