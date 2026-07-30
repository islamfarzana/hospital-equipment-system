from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('equipment-inventory/', views.equipment_inventory_report, name='equipment_inventory'),
    path('equipment-by-department/', views.equipment_by_department_report, name='equipment_by_department'),
    path('maintenance-costs/', views.maintenance_cost_report, name='maintenance_costs'),
    path('allocation-history/', views.allocation_history_report, name='allocation_history'),
    path('faulty-decommissioned/', views.faulty_decommissioned_report, name='faulty_decommissioned'),
    path('calibration-due/', views.calibration_due_report, name='calibration_due'),
]