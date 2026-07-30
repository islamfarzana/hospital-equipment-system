from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import Ward
from .forms import WardForm


@role_required('ADMIN')
def ward_list(request):
    wards = Ward.objects.all()
    return render(request, 'wards/ward_list.html', {'wards': wards})


@role_required('ADMIN')
def ward_add(request):
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward added successfully.')
            return redirect('wards:ward_list')
    else:
        form = WardForm()
    return render(request, 'wards/ward_form.html', {'form': form, 'title': 'Add Ward'})


@role_required('ADMIN')
def ward_edit(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    if request.method == 'POST':
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward updated successfully.')
            return redirect('wards:ward_list')
    else:
        form = WardForm(instance=ward)
    return render(request, 'wards/ward_form.html', {'form': form, 'title': 'Edit Ward'})


@role_required('ADMIN')
def ward_delete(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    if request.method == 'POST':
        ward.delete()
        messages.success(request, 'Ward deleted successfully.')
        return redirect('wards:ward_list')
    return render(request, 'wards/ward_confirm_delete.html', {'ward': ward})