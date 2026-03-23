from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    @property
    def teacher_profile(self):
        if hasattr(self, '_teacher_profile'):
            return self._teacher_profile
        try:
            from faculty.models import Teacher
            self._teacher_profile = Teacher.objects.get(user=self)
            return self._teacher_profile
        except Teacher.DoesNotExist:
            return None

    @property
    def student_profile(self):
        if hasattr(self, '_student_profile'):
            return self._student_profile
        try:
            from student.models import Student
            self._student_profile = Student.objects.get(user=self)
            return self._student_profile
        except Student.DoesNotExist:
            return None

    def __str__(self):
        return self.username
