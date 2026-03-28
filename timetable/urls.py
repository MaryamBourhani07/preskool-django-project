from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.timetable_list, name='timetable_list'),
    path('add/', views.timetable_create, name='timetable_create'),
    path('edit/<int:pk>/', views.timetable_update, name='timetable_update'),
    path('delete/<int:pk>/', views.timetable_delete, name='timetable_delete'),
]
