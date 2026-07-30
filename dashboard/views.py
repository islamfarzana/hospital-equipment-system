from django.shortcuts import render
from accounts.decorators import role_required
from equipment.models import Equipment
from accounts.models import Staff
from requests_app.models import StaffRequest
from allocations.models import EquipmentAllocation
from maintenance.models import MaintenanceRecord


@role_required('ADMIN')
def admin_dashboard(request):
    context = {
        'total_equipment': Equipment.objects.count(),
        'available_equipment': Equipment.objects.filter(current_status='AVAILABLE').count(),
        'allocated_equipment': Equipment.objects.filter(current_status='ALLOCATED').count(),
        'maintenance_equipment': Equipment.objects.filter(current_status='UNDER_MAINTENANCE').count(),
        'faulty_equipment': Equipment.objects.filter(current_status='FAULTY').count(),
        'total_staff': Staff.objects.count(),
        'recent_requests': StaffRequest.objects.select_related('staff').order_by('-created_at')[:5],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@role_required('BIOMEDICAL_OFFICER')
def biomedical_dashboard(request):
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    context = {
        'todays_allocations': EquipmentAllocation.objects.filter(allocated_date=today).count(),
        'pending_requests': StaffRequest.objects.filter(status='PENDING').count(),
        'due_for_return': EquipmentAllocation.objects.filter(
            status='ALLOCATED', expected_return_date__lte=today
        ).count(),
        'calibration_due_soon': Equipment.objects.filter(
            next_calibration_due__lte=today + timedelta(days=30),
            next_calibration_due__gte=today,
        ).count(),
    }
    return render(request, 'dashboard/biomedical_dashboard.html', context)


@role_required('WARD_STAFF')
def ward_staff_dashboard(request):
    staff = getattr(request.user, 'staff_profile', None)
    context = {}
    if staff:
        context['my_equipment'] = EquipmentAllocation.objects.filter(
            ward=staff.ward, status='ALLOCATED'
        ).select_related('equipment') if staff.ward else []
        context['my_requests_count'] = StaffRequest.objects.filter(staff=staff).count()
    return render(request, 'dashboard/ward_staff_dashboard.html', context)