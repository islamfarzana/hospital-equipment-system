from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('add/', views.maintenance_add, name='maintenance_add'),
    path('<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
    path('<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),
]