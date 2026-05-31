from django.contrib import admin

from .models import (
    Student,
    TestResult,
    Activity
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'age',
        'student_class',
        'last_score',
        'created_at'
    )

    search_fields = (
        'name',
        'student_class'
    )


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'score',
        'total',
        'percentage',
        'created_at'
    )

    search_fields = (
        'student__name',
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'message',
        'created_at'
    )