from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('biomedical/', views.biomedical_dashboard, name='biomedical_dashboard'),
    path('ward-staff/', views.ward_staff_dashboard, name='ward_staff_dashboard'),
]