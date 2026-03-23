from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .models import Department, Teacher, Subject, Holiday, TimeTable, Exam, ExamResult
from home_auth.models import CustomUser
from student.models import Student
from django.db.models import Q
from django.core.paginator import Paginator
import json


# Create your views here.
def index(request):
    return render(request, 'Home/index.html')


def dashboard(request):
    # Redirect to teacher dashboard if user is teacher
    if request.user.is_authenticated and request.user.is_teacher:
        return redirect('authentication:teacher_dashboard')
    # Otherwise redirect to admin dashboard
    return redirect('faculty:index')


# Teachers Views
@login_required
def teacher_list(request):
    if not (request.user.is_admin or request.user.is_teacher):
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    teachers = Teacher.objects.select_related('department', 'user').filter(is_active=True)
    query = request.GET.get('q')
    if query:
        teachers = teachers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(department__name__icontains=query)
        )

    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'teachers': page_obj,
        'query': query,
    }
    return render(request, 'Home/teacher-list.html', context)


@login_required
def teacher_details(request, teacher_id):
    if not (request.user.is_admin or request.user.is_teacher):
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    context = {'teacher': teacher}
    return render(request, 'Home/teacher-details.html', context)


@login_required
def add_teacher(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            employee_id = request.POST.get('employee_id')
            phone = request.POST.get('phone')
            department_id = request.POST.get('department')
            qualification = request.POST.get('qualification')
            experience_years = request.POST.get('experience_years', 0)
            joining_date = request.POST.get('joining_date')
            salary = request.POST.get('salary', 0)
            address = request.POST.get('address')
            teacher_image = request.FILES.get('teacher_image')

            # Create user account
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='default123'  # Should be changed by teacher
            )
            user.is_teacher = True
            user.save()

            # Create teacher profile
            department = None
            if department_id:
                department = Department.objects.get(id=department_id)

            teacher = Teacher.objects.create(
                user=user,
                employee_id=employee_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                department=department,
                qualification=qualification,
                experience_years=experience_years,
                joining_date=joining_date,
                salary=salary,
                address=address,
                teacher_image=teacher_image,
            )

            messages.success(request, f'Teacher {teacher} added successfully!')
            return redirect('faculty:teacher_list')

        except Exception as e:
            messages.error(request, f'Error adding teacher: {str(e)}')
            return redirect('faculty:add_teacher')

    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, 'Home/teacher-add.html', context)


@login_required
def edit_teacher(request, teacher_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == 'POST':
        try:
            # Update teacher data
            teacher.first_name = request.POST.get('first_name')
            teacher.last_name = request.POST.get('last_name')
            teacher.email = request.POST.get('email')
            teacher.phone = request.POST.get('phone')
            department_id = request.POST.get('department')
            teacher.qualification = request.POST.get('qualification')
            teacher.experience_years = request.POST.get('experience_years', 0)
            teacher.salary = request.POST.get('salary', 0)
            teacher.address = request.POST.get('address')

            if department_id:
                teacher.department = Department.objects.get(id=department_id)
            else:
                teacher.department = None

            if request.FILES.get('teacher_image'):
                teacher.teacher_image = request.FILES.get('teacher_image')

            teacher.save()

            # Update user data
            teacher.user.first_name = teacher.first_name
            teacher.user.last_name = teacher.last_name
            teacher.user.email = teacher.email
            teacher.user.save()

            messages.success(request, f'Teacher {teacher} updated successfully!')
            return redirect('faculty:teacher_list')

        except Exception as e:
            messages.error(request, f'Error updating teacher: {str(e)}')
            return redirect('faculty:edit_teacher', teacher_id=teacher_id)

    departments = Department.objects.all()
    context = {
        'teacher': teacher,
        'departments': departments
    }
    return render(request, 'Home/teacher-edit.html', context)


@login_required
def delete_teacher(request, teacher_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_name = str(teacher)
    teacher.is_active = False
    teacher.save()

    messages.success(request, f'Teacher {teacher_name} deactivated successfully!')
    return redirect('faculty:teacher_list')


# Departments Views
@login_required
def department_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    departments = Department.objects.prefetch_related('teachers').all()
    query = request.GET.get('q')
    if query:
        departments = departments.filter(name__icontains=query)

    paginator = Paginator(departments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'departments': page_obj,
        'query': query,
    }
    return render(request, 'Home/department-list.html', context)


@login_required
def add_department(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            description = request.POST.get('description', '')

            department = Department.objects.create(
                name=name,
                description=description,
            )

            messages.success(request, f'Department {department.name} added successfully!')
            return redirect('faculty:department_list')

        except Exception as e:
            messages.error(request, f'Error adding department: {str(e)}')
            return redirect('faculty:add_department')

    context = {}
    return render(request, 'Home/department-add.html', context)


@login_required
def edit_department(request, department_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    department = get_object_or_404(Department, id=department_id)

    if request.method == 'POST':
        try:
            department.name = request.POST.get('name')
            department.description = request.POST.get('description', '')
            department.save()

            messages.success(request, f'Department {department.name} updated successfully!')
            return redirect('faculty:department_list')

        except Exception as e:
            messages.error(request, f'Error updating department: {str(e)}')
            return redirect('faculty:edit_department', department_id=department_id)

    context = {'department': department}
    return render(request, 'Home/department-edit.html', context)


@login_required
def delete_department(request, department_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    department = get_object_or_404(Department, id=department_id)
    department_name = department.name
    department.delete()

    messages.success(request, f'Department {department_name} deleted successfully!')
    return redirect('faculty:department_list')


# Subjects Views
@login_required
def subject_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    subjects = Subject.objects.select_related('department', 'teacher').filter(is_active=True)
    query = request.GET.get('q')
    if query:
        subjects = subjects.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(department__name__icontains=query)
        )

    paginator = Paginator(subjects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'subjects': page_obj,
        'query': query,
    }
    return render(request, 'Home/subject-list.html', context)


@login_required
def add_subject(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            code = request.POST.get('code')
            description = request.POST.get('description', '')
            department_id = request.POST.get('department')
            teacher_id = request.POST.get('teacher')
            credits = request.POST.get('credits', 1)
            semester = request.POST.get('semester', '')

            department = Department.objects.get(id=department_id)
            teacher = None
            if teacher_id:
                teacher = Teacher.objects.get(id=teacher_id)

            subject = Subject.objects.create(
                name=name,
                code=code,
                description=description,
                department=department,
                teacher=teacher,
                credits=credits,
                semester=semester,
            )

            messages.success(request, f'Subject {subject.name} added successfully!')
            return redirect('faculty:subject_list')

        except Exception as e:
            messages.error(request, f'Error adding subject: {str(e)}')
            return redirect('faculty:add_subject')

    departments = Department.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    context = {
        'departments': departments,
        'teachers': teachers,
    }
    return render(request, 'Home/subject-add.html', context)


@login_required
def edit_subject(request, subject_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        try:
            subject.name = request.POST.get('name')
            subject.code = request.POST.get('code')
            subject.description = request.POST.get('description', '')
            department_id = request.POST.get('department')
            teacher_id = request.POST.get('teacher')
            subject.credits = request.POST.get('credits', 1)
            subject.semester = request.POST.get('semester', '')

            subject.department = Department.objects.get(id=department_id)
            if teacher_id:
                subject.teacher = Teacher.objects.get(id=teacher_id)
            else:
                subject.teacher = None

            subject.save()

            messages.success(request, f'Subject {subject.name} updated successfully!')
            return redirect('faculty:subject_list')

        except Exception as e:
            messages.error(request, f'Error updating subject: {str(e)}')
            return redirect('faculty:edit_subject', subject_id=subject_id)

    departments = Department.objects.all()
    teachers = Teacher.objects.filter(is_active=True)
    context = {
        'subject': subject,
        'departments': departments,
        'teachers': teachers,
    }
    return render(request, 'Home/subject-edit.html', context)


@login_required
def delete_subject(request, subject_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    subject = get_object_or_404(Subject, id=subject_id)
    subject_name = str(subject)
    subject.delete()

    messages.success(request, f'Subject {subject_name} deleted successfully!')
    return redirect('faculty:subject_list')


# Holiday Views
@login_required
def holiday_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    holidays = Holiday.objects.filter(is_active=True).order_by('holiday_date')
    query = request.GET.get('q')
    if query:
        holidays = holidays.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(holidays, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'holidays': page_obj,
        'query': query,
    }
    return render(request, 'Home/index.html', context)


# Time Table Views
@login_required
def time_table_list(request):
    if not (request.user.is_admin or request.user.is_teacher):
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    timetable = TimeTable.objects.select_related('subject', 'teacher').filter(is_active=True)
    if request.user.is_teacher:
        timetable = timetable.filter(teacher__user=request.user)

    query = request.GET.get('q')
    if query:
        timetable = timetable.filter(
            Q(subject__name__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        )

    paginator = Paginator(timetable, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'timetable': page_obj,
        'query': query,
    }
    return render(request, 'Home/index.html', context)


# Exam Views
@login_required
def exam_list(request):
    if not (request.user.is_admin or request.user.is_teacher):
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    exams = Exam.objects.select_related('subject', 'teacher').filter(is_active=True)
    if request.user.is_teacher:
        exams = exams.filter(teacher__user=request.user)

    query = request.GET.get('q')
    if query:
        exams = exams.filter(
            Q(title__icontains=query) |
            Q(subject__name__icontains=query)
        )

    paginator = Paginator(exams, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'exams': page_obj,
        'query': query,
    }
    return render(request, 'Home/index.html', context)


# Fees Views
@login_required
def fees_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


@login_required
def fees_collection_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


@login_required
def add_fees_collection(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


# Expenses Views
@login_required
def expenses_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


@login_required
def add_expenses(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


# Salary Views
@login_required
def salary_list(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


@login_required
def add_salary(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('faculty:index')

    return render(request, 'Home/index.html')


# Other Views
def event_list(request):
    return render(request, 'Home/index.html')


def library_list(request):
    return render(request, 'Home/index.html')


def sports_list(request):
    return render(request, 'Home/index.html')


def hostel_list(request):
    return render(request, 'Home/index.html')


def transport_list(request):
    return render(request, 'Home/index.html')


def components_list(request):
    return render(request, 'Home/index.html')


def login_page(request):
    return render(request, 'authentication/login.html')


def register_page(request):
    return render(request, 'authentication/register.html')


def forgot_password_page(request):
    return render(request, 'authentication/forgot-password.html')


def error_404(request):
    return render(request, 'Home/index.html')
