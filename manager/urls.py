from django.urls import path
from . import views

urlpatterns = [

    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),

    path('all_student/', views.all_student, name='all_student'),

    path('teacher_list/', views.teacher_list, name='teacher_list'),

    path('parent_list/', views.parent_list, name='parent_list'),

    path('view_report/', views.view_report, name='view_report'),

]