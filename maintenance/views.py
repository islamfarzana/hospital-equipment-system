from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import MaintenanceRecord
from .forms import MaintenanceRecordForm
from django.db import models


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def maintenance_list(request):
    records = MaintenanceRecord.objects.select_related('equipment', 'vendor').all()
    search_query = request.GET.get('q', '').strip()
    if search_query:
        records = records.filter(
            models.Q(equipment__equipment_name__icontains=search_query) |
            models.Q(equipment__equipment_code__icontains=search_query) |
            models.Q(issue_description__icontains=search_query)
        )
    return render(request, 'maintenance/maintenance_list.html', {'records': records, 'search_query': search_query})

@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def maintenance_add(request):
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            messages.success(request, 'Maintenance record added successfully.')
            return redirect('maintenance:maintenance_list')
    else:
        form = MaintenanceRecordForm()
    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'title': 'Add Maintenance Record'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def maintenance_edit(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record updated successfully.')
            return redirect('maintenance:maintenance_list')
    else:
        form = MaintenanceRecordForm(instance=record)
    return render(request, 'maintenance/maintenance_form.html', {'form': form, 'title': 'Edit Maintenance Record'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def maintenance_delete(request, pk):
    record = get_object_or_404(MaintenanceRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Maintenance record deleted successfully.')
        return redirect('maintenance:maintenance_list')
    return render(request, 'maintenance/maintenance_confirm_delete.html', {'record': record})