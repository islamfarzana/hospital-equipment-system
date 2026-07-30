from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')


@login_required
def biomedical_dashboard(request):
    return render(request, 'dashboard/biomedical_dashboard.html')


@login_required
def ward_staff_dashboard(request):
    return render(request, 'dashboard/ward_staff_dashboard.html')