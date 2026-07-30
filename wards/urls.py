from django.urls import path
from . import views

app_name = 'wards'

urlpatterns = [
    path('', views.ward_list, name='ward_list'),
    path('add/', views.ward_add, name='ward_add'),
    path('<int:pk>/edit/', views.ward_edit, name='ward_edit'),
    path('<int:pk>/delete/', views.ward_delete, name='ward_delete'),
]