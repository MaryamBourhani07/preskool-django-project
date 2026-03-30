from django.contrib import admin
from .models import Exam

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'student', 'date', 'score')
    list_filter = ('subject', 'date')
    search_fields = ('subject', 'student__first_name', 'student__last_name')
