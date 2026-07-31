from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .decorators import role_required
from .forms import LoginForm, StaffForm
from .models import Staff

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return reverse_lazy('dashboard:admin_dashboard')
        elif user.role == 'BIOMEDICAL_OFFICER':
            return reverse_lazy('dashboard:biomedical_dashboard')
        else:
            return reverse_lazy('dashboard:ward_staff_dashboard')


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@role_required('ADMIN')
def staff_list(request):
    staff_qs = Staff.objects.select_related('user', 'ward', 'designation').all()
    search_query = request.GET.get('q', '').strip()
    if search_query:
        staff_qs = staff_qs.filter(
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(staff_code__icontains=search_query)
        )
    return render(request, 'accounts/staff_list.html', {'staff_list': staff_qs, 'search_query': search_query})


@role_required('ADMIN')
def staff_add(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff added successfully.')
            return redirect('accounts:staff_list')
    else:
        form = StaffForm()
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Add Staff'})


@role_required('ADMIN')
def staff_edit(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated successfully.')
            return redirect('accounts:staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Edit Staff'})


@role_required('ADMIN')
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, 'Staff deleted successfully.')
        return redirect('accounts:staff_list')
    return render(request, 'accounts/staff_confirm_delete.html', {'staff': staff})