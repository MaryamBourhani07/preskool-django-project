from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam
from .forms import ExamForm
from django.contrib import messages

def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exam/exam_list.html', {'exams': exams})

def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully!')
            return redirect('exam:exam_list')
    else:
        form = ExamForm()
    return render(request, 'exam/exam_form.html', {'form': form, 'title': 'Add Exam'})

def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully!')
            return redirect('exam:exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exam/exam_form.html', {'form': form, 'title': 'Edit Exam'})

def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully!')
        return redirect('exam:exam_list')
    return render(request, 'exam/exam_confirm_delete.html', {'exam': exam})
