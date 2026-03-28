from django.db import models
from student.models import Student

class Exam(models.Model):
    subject = models.CharField(max_length=100)
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams')
    score = models.FloatField()

    def __str__(self):
        return f"{self.subject} - {self.student.first_name} ({self.score})"

    class Meta:
        ordering = ['-date']
