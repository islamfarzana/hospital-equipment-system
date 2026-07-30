from django.urls import path
from . import views

app_name = 'requests_app'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('add/', views.request_add, name='request_add'),
    path('<int:pk>/review/', views.request_review, name='request_review'),
]