from django.db import models


class MaintenanceRecord(models.Model):
    class MaintenanceStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    equipment = models.ForeignKey(
        'equipment.Equipment',
        on_delete=models.CASCADE,
        related_name='maintenance_records',
    )
    vendor = models.ForeignKey(
        'equipment.Vendor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_records',
    )
    issue_description = models.TextField()
    maintenance_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    maintenance_status = models.CharField(
        max_length=15,
        choices=MaintenanceStatus.choices,
        default=MaintenanceStatus.PENDING,
    )
    calibration_certificate_ref = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='maintenance_records_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.equipment} - {self.maintenance_status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.maintenance_status in [self.MaintenanceStatus.PENDING, self.MaintenanceStatus.IN_PROGRESS]:
            self.equipment.current_status = 'UNDER_MAINTENANCE'
        elif self.maintenance_status == self.MaintenanceStatus.COMPLETED:
            self.equipment.current_status = 'AVAILABLE'
        self.equipment.save()