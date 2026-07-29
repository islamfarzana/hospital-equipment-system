from django.db import models


class EquipmentCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['category_name']
        verbose_name_plural = 'Equipment Categories'

    def __str__(self):
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['brand_name']

    def __str__(self):
        return self.brand_name


class Vendor(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    vendor_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        ordering = ['vendor_name']

    def __str__(self):
        return self.vendor_name

class Equipment(models.Model):
    class EquipmentType(models.TextChoices):
        VENTILATOR = 'VENTILATOR', 'Ventilator'
        INFUSION_PUMP = 'INFUSION_PUMP', 'Infusion Pump'
        ECG_MACHINE = 'ECG_MACHINE', 'ECG Machine'
        PATIENT_MONITOR = 'PATIENT_MONITOR', 'Patient Monitor'
        WHEELCHAIR = 'WHEELCHAIR', 'Wheelchair'
        DEFIBRILLATOR = 'DEFIBRILLATOR', 'Defibrillator'
        OXYGEN_CONCENTRATOR = 'OXYGEN_CONCENTRATOR', 'Oxygen Concentrator'
        HOSPITAL_BED = 'HOSPITAL_BED', 'Hospital Bed'

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        ALLOCATED = 'ALLOCATED', 'Allocated'
        UNDER_MAINTENANCE = 'UNDER_MAINTENANCE', 'Under Maintenance'
        FAULTY = 'FAULTY', 'Faulty'
        DECOMMISSIONED = 'DECOMMISSIONED', 'Decommissioned'

    equipment_code = models.CharField(max_length=30, unique=True, editable=False)
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.PROTECT,
        related_name='equipment_items',
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipment_items',
    )
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment_items',
    )
    equipment_name = models.CharField(max_length=150)
    equipment_type = models.CharField(max_length=30, choices=EquipmentType.choices)
    model = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
    warranty_expiry = models.DateField(null=True, blank=True)
    last_calibration_date = models.DateField(null=True, blank=True)
    next_calibration_due = models.DateField(null=True, blank=True)
    current_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_code})"

    def save(self, *args, **kwargs):
        if not self.equipment_code:
            last_equipment = Equipment.objects.order_by('id').last()
            next_id = (last_equipment.id + 1) if last_equipment else 1
            self.equipment_code = f"EQP-{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_code})"

class EquipmentAuditLog(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='audit_logs',
    )
    action = models.CharField(max_length=100)
    performed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='equipment_actions',
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Equipment Audit Logs'

    def __str__(self):
        return f"{self.equipment} - {self.action} ({self.created_at:%Y-%m-%d %H:%M})"