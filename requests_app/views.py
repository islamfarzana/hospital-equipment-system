from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import role_required
from .models import StaffRequest
from .forms import StaffRequestForm, StaffRequestReviewForm


@role_required('ADMIN', 'BIOMEDICAL_OFFICER', 'WARD_STAFF')
def request_list(request):
    user = request.user
    if user.role == 'WARD_STAFF':
        requests_qs = StaffRequest.objects.filter(staff__user=user)
    else:
        requests_qs = StaffRequest.objects.select_related('staff', 'equipment').all()
    return render(request, 'requests_app/request_list.html', {'requests': requests_qs})


@role_required('WARD_STAFF')
def request_add(request):
    if request.method == 'POST':
        form = StaffRequestForm(request.POST)
        if form.is_valid():
            staff_request = form.save(commit=False)
            staff_request.staff = request.user.staff_profile
            staff_request.save()
            messages.success(request, 'Request submitted successfully.')
            return redirect('requests_app:request_list')
    else:
        form = StaffRequestForm()
    return render(request, 'requests_app/request_form.html', {'form': form, 'title': 'New Request'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def request_review(request, pk):
    staff_request = get_object_or_404(StaffRequest, pk=pk)
    if request.method == 'POST':
        form = StaffRequestReviewForm(request.POST, instance=staff_request)
        if form.is_valid():
            reviewed_request = form.save(commit=False)
            reviewed_request.approved_by = request.user
            reviewed_request.approved_at = timezone.now()
            reviewed_request.save()
            messages.success(request, 'Request status updated successfully.')
            return redirect('requests_app:request_list')
    else:
        form = StaffRequestReviewForm(instance=staff_request)
    return render(request, 'requests_app/request_review.html', {'form': form, 'staff_request': staff_request})