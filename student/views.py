from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Student, Parent
from django.contrib import messages


def student_list(request):
    students = Student.objects.all()
    return render(request, 'students/students.html', {'student_list': students})


def add_student(request):
    if request.method == 'POST':
        # Get student data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_class = request.POST.get('student_class')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Get parent data
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')
        
        # Create parent
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )
        
        # Create student
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )
        
        messages.success(request, 'Student added successfully')
        return redirect('student:student_list')
    
    return render(request, 'students/add-student.html')


def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    
    if request.method == 'POST':
        # Update student data
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.student_class = request.POST.get('student_class')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')
        
        # Update parent data
        student.parent.father_name = request.POST.get('father_name')
        student.parent.father_occupation = request.POST.get('father_occupation')
        student.parent.father_mobile = request.POST.get('father_mobile')
        student.parent.father_email = request.POST.get('father_email')
        student.parent.mother_name = request.POST.get('mother_name')
        student.parent.mother_occupation = request.POST.get('mother_occupation')
        student.parent.mother_mobile = request.POST.get('mother_mobile')
        student.parent.mother_email = request.POST.get('mother_email')
        student.parent.present_address = request.POST.get('present_address')
        student.parent.permanent_address = request.POST.get('permanent_address')
        
        student.parent.save()
        student.save()
        
        messages.success(request, 'Student updated successfully')
        return redirect('student:student_list')
    
    context = {'student': student}
    return render(request, 'students/edit-student.html', context)


def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    context = {'student': student}
    return render(request, 'students/student-details.html', context)


def delete_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, student_id=student_id)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully')
    return redirect('student:student_list')