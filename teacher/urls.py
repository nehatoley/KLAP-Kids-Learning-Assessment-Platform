from django.urls import path
from . import views

urlpatterns = [
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('student_list', views.student_list, name="student_list"),
    path('add_student/', views.add_student, name="add_student"),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('start-learning/<int:student_id>/', views.start_learning, name='start_learning'),
    path('quiz/<int:student_id>/', views.quiz_question, name='quiz_question'),
    path('submit-test/<int:student_id>/', views.submit_test, name='submit_test'),
    path('report/', views.report, name="report"),
]