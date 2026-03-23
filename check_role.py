import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
import django
django.setup()
from home_auth.models import CustomUser
users = CustomUser.objects.filter(email__icontains='maryam')
print('Maryam users:')
for u in users:
    print(u.email, 'is_teacher', u.is_teacher, 'is_student', u.is_student, 'is_admin', u.is_admin)
print('Total teachers:', CustomUser.objects.filter(is_teacher=True).count())
