from django.urls import path
from . import views

app_name = 'exam'

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('add/', views.exam_create, name='exam_create'),
    path('edit/<int:pk>/', views.exam_update, name='exam_update'),
    path('delete/<int:pk>/', views.exam_delete, name='exam_delete'),
]
