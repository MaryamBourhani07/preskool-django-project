from django.urls import path
from . import views

app_name = 'holiday'

urlpatterns = [
    path('', views.holiday_list, name='holiday_list'),
    path('add/', views.holiday_create, name='holiday_create'),
    path('edit/<int:pk>/', views.holiday_update, name='holiday_update'),
    path('delete/<int:pk>/', views.holiday_delete, name='holiday_delete'),
]
