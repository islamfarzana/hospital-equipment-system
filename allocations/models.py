from django.db import models
from django.core.exceptions import ValidationError


class EquipmentAllocation(models.Model):
    class Status(models.TextChoices):
        ALLOCATED = 'ALLOCATED', 'Allocated'
        RETURNED = 'RETURNED', 'Returned'

    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.CASCADE,
        related_name='allocations',
    )
    ward = models.ForeignKey(
        'wards.Ward',
        on_delete=models.CASCADE,
        related_name='allocations',
    )
    allocated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='allocations_made',
    )
    allocated_date = models.DateField()
    expected_return_date = models.DateField(null=True, blank=True)
    returned_date = models.DateField(null=True, blank=True)
    return_condition = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ALLOCATED,
    )
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.status == self.Status.ALLOCATED:
            if self.equipment.current_status in ['UNDER_MAINTENANCE', 'FAULTY', 'DECOMMISSIONED']:
                raise ValidationError(
                    f"Cannot allocate equipment with status '{self.equipment.current_status}'."
                )

            existing_active_allocation = EquipmentAllocation.objects.filter(
                equipment=self.equipment,
                status=self.Status.ALLOCATED,
            ).exclude(pk=self.pk)

            if existing_active_allocation.exists():
                raise ValidationError(
                    "This equipment is already actively allocated to another ward."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        if self.status == self.Status.ALLOCATED:
            self.equipment.current_status = 'ALLOCATED'
        elif self.status == self.Status.RETURNED:
            self.equipment.current_status = 'AVAILABLE'
        self.equipment.save()

    class Meta:
        ordering = ['-allocated_date']

    def __str__(self):
        return f"{self.equipment} → {self.ward} ({self.status})"