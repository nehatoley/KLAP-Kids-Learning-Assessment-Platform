from django.db import models
from user.models import CustomUser


# ===============================
# STUDENT MODEL
# ===============================

class Student(models.Model):

    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='students',
        limit_choices_to={'role': 'teacher'},
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    age = models.IntegerField()

    student_class = models.CharField(
        max_length=20
    )

    last_score = models.IntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


# ===============================
# TEST RESULT HISTORY
# ===============================

class TestResult(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    total = models.IntegerField()

    percentage = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.student.name} - {self.percentage}%"


# ===============================
# ACTIVITY MODEL
# ===============================

class Activity(models.Model):

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.message