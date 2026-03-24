from django.contrib import admin
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
path('signup/', views.signup_view, name='signup'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('forgot-password/', views.forgot_password, name='forgot-password'),
path('dashboard/', views.student_dashboard, name='dashboard'),        
path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),       
]
