from django.db import models
from django.contrib.auth import get_user_model
from home_auth.models import CustomUser

User = get_user_model()

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.OneToOneField(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='department_head'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='teachers'
    )
    qualification = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField(default=0)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teachers/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    credits = models.PositiveIntegerField(default=1)
    semester = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        unique_together = ['code', 'department']


class Holiday(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    holiday_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # For multi-day holidays
    holiday_type = models.CharField(
        max_length=20,
        choices=[
            ('National', 'National Holiday'),
            ('Religious', 'Religious Holiday'),
            ('School', 'School Holiday'),
            ('Other', 'Other')
        ],
        default='School'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.holiday_date}"

    class Meta:
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"
        ordering = ['holiday_date']


class TimeTable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='timetable_entries'
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    classroom = models.CharField(max_length=50)
    semester = models.CharField(max_length=50, blank=True)
    academic_year = models.CharField(max_length=20, default='2024-2025')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject.name} - {self.day_of_week} {self.start_time}-{self.end_time}"

    class Meta:
        verbose_name = "Time Table Entry"
        verbose_name_plural = "Time Table"
        ordering = ['day_of_week', 'start_time']
        unique_together = ['subject', 'teacher', 'day_of_week', 'start_time', 'academic_year']


class Exam(models.Model):
    EXAM_TYPES = [
        ('Midterm', 'Midterm Exam'),
        ('Final', 'Final Exam'),
        ('Quiz', 'Quiz'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
    ]

    title = models.CharField(max_length=200)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='exams'
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='exams'
    )
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='Midterm')
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    classroom = models.CharField(max_length=50, blank=True)
    instructions = models.TextField(blank=True)
    semester = models.CharField(max_length=50, blank=True)
    academic_year = models.CharField(max_length=20, default='2024-2025')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.exam_date})"

    class Meta:
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ['exam_date', 'start_time']


class ExamResult(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='results'
    )
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='exam_results'
    )
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=5, blank=True)
    remarks = models.TextField(blank=True)
    is_pass = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.exam.title}: {self.marks_obtained}/{self.exam.total_marks}"

    def save(self, *args, **kwargs):
        # Calculate grade and pass status
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        if percentage >= 90:
            self.grade = 'A+'
        elif percentage >= 80:
            self.grade = 'A'
        elif percentage >= 70:
            self.grade = 'B+'
        elif percentage >= 60:
            self.grade = 'B'
        elif percentage >= 50:
            self.grade = 'C'
        elif percentage >= 40:
            self.grade = 'D'
        else:
            self.grade = 'F'

        self.is_pass = self.marks_obtained >= self.exam.passing_marks
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"
        unique_together = ['exam', 'student']
