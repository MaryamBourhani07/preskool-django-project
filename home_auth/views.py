from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from student.models import Student
from faculty.models import Teacher, Exam, TimeTable


# Create your views here.
@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST.get('role')  # student, teacher or admin
        
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect('authentication:signup')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "L'email existe déjà")
            return redirect('authentication:signup')
        
        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        # Assign role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True
        else:
            user.is_student = True  # By default, assign student role
        
        user.save()
        
        # Create profile based on role
        if role == 'teacher':
            from datetime import date
            Teacher.objects.create(
                user=user,
                employee_id=f"EMP{user.id:04d}",
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone="",  # Empty for now, can be updated later
                qualification="",
                experience_years=0,
                joining_date=date.today(),
                salary=0,
                address=""
            )
        
        # Authenticate + login
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
        
        messages.success(request, 'Inscription réussie !')
        # Redirection based on role
        if user.is_admin:
            return redirect('authentication:admin_dashboard')
        elif user.is_teacher:
            return redirect('authentication:teacher_dashboard')
        elif user.is_student:
            return redirect('authentication:dashboard')
        else:
            messages.error(request, 'Rôle utilisateur invalide')
            return redirect('authentication:login')
    
    return render(request, 'authentication/register.html')


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            # Redirection based on role
            if user.is_admin:
                return redirect('authentication:admin_dashboard')
            elif user.is_teacher:
                return redirect('authentication:teacher_dashboard')
            elif user.is_student:
                return redirect('authentication:dashboard')
            else:
                messages.error(request, 'Rôle utilisateur invalide')
                return redirect('authentication:login')
        else:
            messages.error(request, 'Identifiants invalides')
    
    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('authentication:login')


def forgot_password(request):
    return render(request, 'authentication/forgot-password.html')


def student_dashboard(request):
    return render(request, 'students/student-dashboard.html')


@login_required
def teacher_dashboard(request):
    # If user should be treated as teacher based on linked Teacher model, auto-assign flag
    if not request.user.is_teacher:
        teacher_profile = request.user.teacher_profile
        if teacher_profile:
            request.user.is_teacher = True
            request.user.save(update_fields=['is_teacher'])
        else:
            messages.error(request, 'Accès refusé. Accès enseignant requis.')
            return redirect('authentication:login')

    # Get teacher profile
    try:
        teacher = request.user.teacher_profile
        if teacher is None:
            messages.error(request, 'Profil enseignant introuvable.')
            return redirect('authentication:login')
    except:
        messages.error(request, 'Profil enseignant introuvable.')
        return redirect('authentication:login')

    # Get statistics
    # Count all students (since student_class doesn't match subject names)
    total_students = Student.objects.count()
    
    # Safely count subjects
    if hasattr(teacher, 'subjects') and teacher.subjects is not None:
        total_subjects = teacher.subjects.count()
    else:
        total_subjects = 0
        
    total_exams = Exam.objects.filter(teacher=teacher).count()
    total_timetable = TimeTable.objects.filter(teacher=teacher).count()

    context = {
        'teacher': teacher,
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_exams': total_exams,
        'total_timetable': total_timetable,
    }
    return render(request, 'dashboard/teacher.html', context)


def admin_dashboard(request):
    return render(request, 'Home/index.html')