from django.contrib import admin
from .models import Timetable

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day', 'subject', 'teacher', 'start_time', 'end_time')
    list_filter = ('day', 'teacher')
    search_fields = ('subject', 'teacher')
