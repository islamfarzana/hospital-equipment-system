import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from accounts.decorators import role_required
from equipment.models import Equipment
from allocations.models import EquipmentAllocation
from maintenance.models import MaintenanceRecord


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def reports_home(request):
    return render(request, 'reports/reports_home.html')


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_inventory_report(request):
    equipment_qs = Equipment.objects.select_related('category', 'brand', 'vendor').all()

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="equipment_inventory.csv"'
        writer = csv.writer(response)
        writer.writerow(['Code', 'Name', 'Type', 'Category', 'Brand', 'Serial Number', 'Status', 'Purchase Cost'])
        for item in equipment_qs:
            writer.writerow([
                item.equipment_code, item.equipment_name, item.get_equipment_type_display(),
                item.category, item.brand, item.serial_number, item.current_status, item.purchase_cost,
            ])
        return response

    return render(request, 'reports/equipment_inventory.html', {'equipment_list': equipment_qs})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def equipment_by_department_report(request):
    allocations = EquipmentAllocation.objects.filter(status='ALLOCATED').select_related('equipment', 'ward')

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="equipment_by_department.csv"'
        writer = csv.writer(response)
        writer.writerow(['Ward', 'Equipment', 'Allocated Date', 'Expected Return'])
        for alloc in allocations:
            writer.writerow([alloc.ward, alloc.equipment, alloc.allocated_date, alloc.expected_return_date])
        return response

    return render(request, 'reports/equipment_by_department.html', {'allocations': allocations})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def maintenance_cost_report(request):
    records = MaintenanceRecord.objects.select_related('equipment', 'vendor').all()

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="maintenance_costs.csv"'
        writer = csv.writer(response)
        writer.writerow(['Equipment', 'Vendor', 'Issue', 'Cost', 'Start Date', 'End Date', 'Status'])
        for record in records:
            writer.writerow([
                record.equipment, record.vendor, record.issue_description,
                record.maintenance_cost, record.start_date, record.end_date, record.maintenance_status,
            ])
        return response

    return render(request, 'reports/maintenance_costs.html', {'records': records})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def allocation_history_report(request):
    allocations = EquipmentAllocation.objects.select_related('equipment', 'ward').all()

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="allocation_history.csv"'
        writer = csv.writer(response)
        writer.writerow(['Equipment', 'Ward', 'Allocated Date', 'Returned Date', 'Status'])
        for alloc in allocations:
            writer.writerow([alloc.equipment, alloc.ward, alloc.allocated_date, alloc.returned_date, alloc.status])
        return response

    return render(request, 'reports/allocation_history.html', {'allocations': allocations})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def faulty_decommissioned_report(request):
    equipment_qs = Equipment.objects.filter(current_status__in=['FAULTY', 'DECOMMISSIONED'])

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="faulty_decommissioned.csv"'
        writer = csv.writer(response)
        writer.writerow(['Code', 'Name', 'Status', 'Remarks'])
        for item in equipment_qs:
            writer.writerow([item.equipment_code, item.equipment_name, item.current_status, item.remarks])
        return response

    return render(request, 'reports/faulty_decommissioned.html', {'equipment_list': equipment_qs})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def calibration_due_report(request):
    today = timezone.now().date()
    equipment_qs = Equipment.objects.filter(
        next_calibration_due__lte=today + timedelta(days=30)
    ).exclude(next_calibration_due__isnull=True)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="calibration_due.csv"'
        writer = csv.writer(response)
        writer.writerow(['Code', 'Name', 'Last Calibration', 'Next Calibration Due'])
        for item in equipment_qs:
            writer.writerow([item.equipment_code, item.equipment_name, item.last_calibration_date, item.next_calibration_due])
        return response

    return render(request, 'reports/calibration_due.html', {'equipment_list': equipment_qs})