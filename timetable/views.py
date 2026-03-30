from django.shortcuts import render, redirect, get_object_or_404
from .models import Timetable
from .forms import TimetableForm
from django.contrib import messages

def timetable_list(request):
    # Group by day as requested
    timetable_data = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days:
        entries = Timetable.objects.filter(day=day)
        if entries.exists():
            timetable_data[day] = entries
            
    return render(request, 'timetable/timetable_list.html', {'timetable_data': timetable_data})

def timetable_create(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry added!')
            return redirect('timetable:timetable_list')
    else:
        form = TimetableForm()
    return render(request, 'timetable/timetable_form.html', {'form': form, 'title': 'Add Timetable Entry'})

def timetable_update(request, pk):
    entry = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry updated!')
            return redirect('timetable:timetable_list')
    else:
        form = TimetableForm(instance=entry)
    return render(request, 'timetable/timetable_form.html', {'form': form, 'title': 'Edit Timetable Entry'})

def timetable_delete(request, pk):
    entry = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted!')
        return redirect('timetable:timetable_list')
    return render(request, 'timetable/timetable_confirm_delete.html', {'entry': entry})
