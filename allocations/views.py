from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import role_required
from .models import EquipmentAllocation
from .forms import EquipmentAllocationForm


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def allocation_list(request):
    allocations = EquipmentAllocation.objects.select_related('equipment', 'ward').all()
    return render(request, 'allocations/allocation_list.html', {'allocations': allocations})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def allocation_add(request):
    if request.method == 'POST':
        form = EquipmentAllocationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Equipment allocated successfully.')
                return redirect('allocations:allocation_list')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EquipmentAllocationForm()
    return render(request, 'allocations/allocation_form.html', {'form': form, 'title': 'Allocate Equipment'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def allocation_edit(request, pk):
    allocation = get_object_or_404(EquipmentAllocation, pk=pk)
    if request.method == 'POST':
        form = EquipmentAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Allocation updated successfully.')
                return redirect('allocations:allocation_list')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EquipmentAllocationForm(instance=allocation)
    return render(request, 'allocations/allocation_form.html', {'form': form, 'title': 'Edit Allocation'})


@role_required('ADMIN', 'BIOMEDICAL_OFFICER')
def allocation_delete(request, pk):
    allocation = get_object_or_404(EquipmentAllocation, pk=pk)
    if request.method == 'POST':
        allocation.delete()
        messages.success(request, 'Allocation record deleted successfully.')
        return redirect('allocations:allocation_list')
    return render(request, 'allocations/allocation_confirm_delete.html', {'allocation': allocation})