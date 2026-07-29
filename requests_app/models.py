from django.db import models


class StaffRequest(models.Model):
    class RequestType(models.TextChoices):
        NEW_EQUIPMENT = 'NEW_EQUIPMENT', 'New Equipment'
        FAULTY_REPORT = 'FAULTY_REPORT', 'Faulty/Damaged Report'
        REPLACEMENT = 'REPLACEMENT', 'Replacement'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'

    staff = models.ForeignKey(
        'accounts.Staff',
        on_delete=models.CASCADE,
        related_name='requests',
    )
    request_type = models.CharField(max_length=20, choices=RequestType.choices)
    equipment_category = models.ForeignKey(
        'equipment.EquipmentCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_requests',
    )
    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_requests',
    )
    description = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requests_approved',
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.staff} - {self.get_request_type_display()} ({self.status})"