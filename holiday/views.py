from django.shortcuts import render, redirect, get_object_or_404
from .models import Holiday
from .forms import HolidayForm
from django.contrib import messages

def holiday_list(request):
    holidays = Holiday.objects.all()
    return render(request, 'holiday/holiday_list.html', {'holidays': holidays})

def holiday_create(request):
    if request.method == 'POST':
        form = HolidayForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Holiday added successfully!')
            return redirect('holiday:holiday_list')
    else:
        form = HolidayForm()
    return render(request, 'holiday/holiday_form.html', {'form': form, 'title': 'Add Holiday'})

def holiday_update(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        form = HolidayForm(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            messages.success(request, 'Holiday updated successfully!')
            return redirect('holiday:holiday_list')
    else:
        form = HolidayForm(instance=holiday)
    return render(request, 'holiday/holiday_form.html', {'form': form, 'title': 'Edit Holiday'})

def holiday_delete(request, pk):
    holiday = get_object_or_404(Holiday, pk=pk)
    if request.method == 'POST':
        holiday.delete()
        messages.success(request, 'Holiday deleted successfully!')
        return redirect('holiday:holiday_list')
    return render(request, 'holiday/holiday_confirm_delete.html', {'holiday': holiday})
