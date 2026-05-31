from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Avg

from detection.models import QuizResult
from user.models import  CustomUser
from teacher.models import TestResult, Student
from parents.models import Child
from django.db.models import Count
from detection.models import (
    UserAnswer,
    QuizResult
)
from teacher.models import (
    Student,
    TestResult
)

from parents.models import Child






# =========================================
# MANAGER DASHBOARD
# =========================================

@login_required
def manager_dashboard(request):

    # 🔍 SEARCH

    search_query = request.GET.get('search')

    if search_query:

        children = Child.objects.filter(
            name__icontains=search_query
        )

    else:

        children = Child.objects.all()


    # =========================================
    # COUNTS
    # =========================================

    total_students = (
            Child.objects.count() +
            Student.objects.count()
    )

    total_teachers = CustomUser.objects.filter(
        role='teacher'
    ).count()

    total_parents = CustomUser.objects.filter(
        role='parent'
    ).count()


    # =========================================
    # STUDENT TABLE DATA
    # =========================================

    data = []

    for child in children:

        latest_result = TestResult.objects.filter(
            student__name=child.name
        ).order_by('-created_at').first()

        data.append({

            'name': child.name,

            'age': child.age,

            'score': (
                latest_result.percentage
                if latest_result else 0
            )

        })

    # =========================================
    # TOP STUDENTS
    # =========================================

    top_students = []

    # Student model results
    student_results = TestResult.objects.all()

    for s in student_results:
        top_students.append({

            "name": s.student.name,

            "score": s.percentage

        })

    # Child model results
    child_results = QuizResult.objects.all()

    for c in child_results:
        top_students.append({

            "name": c.child.name,

            "score": c.score

        })

    # Highest first
    top_students = sorted(

        top_students,

        key=lambda x: x['score'],

        reverse=True

    )[:5]

    # =========================================
    # RECENT TESTS
    # =========================================

    recent_scores = []

    # Student results
    for r in TestResult.objects.all():
        recent_scores.append({

            "name": r.student.name,

            "score": r.percentage,

            "date": r.created_at

        })

    # Child results
    for q in QuizResult.objects.all():
        recent_scores.append({

            "name": q.child.name,

            "score": q.score,

            "date": q.created_at

        })

    recent_scores = sorted(

        recent_scores,

        key=lambda x: x['date'],

        reverse=True

    )[:5]

    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'total_students': total_students,

        'teachers': total_teachers,

        'parents': total_parents,

        'data': data,

        'top_students': top_students,

        'recent_scores': recent_scores,

    }

    return render(
        request,
        'manager_dashboard.html',
        context
    )


# =========================================
# STUDENT LIST
# =========================================


@login_required
def all_student(request):

    children = Child.objects.all()

    students = Student.objects.all()

    total_students = (
        children.count() +
        students.count()
    )

    # =========================
    # TEACHER DATA
    # =========================



    teacher_data = CustomUser.objects.filter(
        role='teacher'
    ).annotate(
        total_students=Count('students')
    )

    # =========================
    # PARENT DATA
    # =========================

    parent_data = CustomUser.objects.filter(
        role='parent'
    ).annotate(
        total_children=Count('children')
    )

    return render(
        request,
        'all_student.html',
        {
            'children': children,
            'students': students,
            'total_students': total_students,
            'teacher_data': teacher_data,
            'parent_data': parent_data,
        }
    )
# =========================================
# TEACHER LIST
# =========================================

@login_required
def teacher_list(request):

    teachers = CustomUser.objects.filter(
        role='teacher'
    ).prefetch_related(
        'students'
    )

    return render(
        request,
        'teacher_list.html',
        {
            'teachers': teachers
        }
    )

# =========================================
# PARENT LIST
# =========================================



@login_required
def parent_list(request):

    parents = CustomUser.objects.filter(
        role='parent'
    ).prefetch_related(
        'children'
    )

    for parent in parents:

        for child in parent.children.all():

            # ANSWERS
            answers = UserAnswer.objects.filter(
                child=child
            )

            # TOTAL LEARNED
            child.total_learned = answers.filter(
                is_correct=True
            ).count()

            # WEAK AREAS
            weak_categories = answers.filter(
                is_correct=False
            ).values_list(
                'question__category',
                flat=True
            ).distinct()

            child.weak_areas = ", ".join(
                [c.capitalize() for c in weak_categories]
            ) if weak_categories else "None"

            # QUIZ RESULTS
            results = QuizResult.objects.filter(
                child=child
            ).order_by('-created_at')

            # TOTAL TESTS
            child.total_tests = results.count()

            # LATEST SCORE
            child.latest_score = (
                results.first().score
                if results.exists()
                else 0
            )

    return render(
        request,
        'parent_list.html',
        {
            'parents': parents
        }
    )

# =========================================
# REPORTS
# =========================================



@login_required
def view_report(request):

    report_data = []


    # =====================================
    # CHILD REPORTS
    # =====================================

    children = Child.objects.all()

    for child in children:

        tests = QuizResult.objects.filter(
            child=child
        ).order_by('-created_at')

        tests_given = tests.count()

        average = 0

        best = 0

        if tests_given > 0:

            average = sum(
                t.score for t in tests
            ) / tests_given

            best = max(
                t.score for t in tests
            )


        # PERFORMANCE

        if average >= 80:

            performance = "Excellent"

        elif average >= 60:

            performance = "Good"

        elif average >= 40:

            performance = "Average"

        else:

            performance = "Poor"


        report_data.append({

            "name": child.name,

            "type": "Child",

            "tests_given": tests_given,

            "average": round(average, 1),

            "best": best,

            "performance": performance,

            "tests": tests

        })


    # =====================================
    # TEACHER STUDENT REPORTS
    # =====================================

    students = Student.objects.all()

    for student in students:

        tests = TestResult.objects.filter(
            student=student
        ).order_by('-created_at')

        tests_given = tests.count()

        average = 0

        best = 0

        if tests_given > 0:

            average = sum(
                t.percentage for t in tests
            ) / tests_given

            best = max(
                t.percentage for t in tests
            )


        # PERFORMANCE

        if average >= 80:

            performance = "Excellent"

        elif average >= 60:

            performance = "Good"

        elif average >= 40:

            performance = "Average"

        else:

            performance = "Poor"


        report_data.append({

            "name": student.name,

            "type": "Student",

            "tests_given": tests_given,

            "average": round(average, 1),

            "best": best,

            "performance": performance,

            "tests": tests

        })



    return render(

        request,

        "view_report.html",

        {
            "reports": report_data
        }
    )