from django.urls import path
from . import views

urlpatterns = [
    path('parent-dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('add-child/', views.add_child, name='add_child'),
    path('camera/', views.parent_camera, name='parent_camera'),
    path('learning/<int:child_id>/', views.learning_view, name='learning'),
    path('quiz/start/<int:child_id>/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:child_id>/', views.quiz_question, name='quiz_question'),
    path('submit/<int:child_id>/', views.submit_answer, name='submit_answer'),
    path('result/<int:child_id>/', views.quiz_result, name='result'),
    path('scores/<int:child_id>/',views.score_view, name='scores'),
]