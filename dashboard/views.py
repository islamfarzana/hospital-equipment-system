from django.shortcuts import render
from accounts.decorators import role_required


@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@role_required('BIOMEDICAL_OFFICER')
def biomedical_dashboard(request):
    return render(request, 'dashboard/biomedical_dashboard.html')


@role_required('WARD_STAFF')
def ward_staff_dashboard(request):
    return render(request, 'dashboard/ward_staff_dashboard.html')