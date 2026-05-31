import random

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg, Max, Min, Count, Q
from django.contrib.auth.decorators import login_required

from .models import Student, TestResult, Activity
from .forms import StudentForm

from detection.models import Question


# =========================================
# DASHBOARD
# =========================================

@login_required
def teacher_dashboard(request):

    total_students = Student.objects.filter(
        teacher=request.user
    ).count()

    avg_score = TestResult.objects.filter(
        student__teacher=request.user
    ).aggregate(
        Avg('percentage')
    )['percentage__avg'] or 0

    latest_students = Student.objects.filter(
        teacher=request.user
    ).order_by('-id')[:5]

    weak_students = Student.objects.filter(
        teacher=request.user,
        last_score__lt=40
    )

    upgrade_students = Student.objects.filter(
        teacher=request.user,
        last_score__gte=80
    )

    inactive_students = Student.objects.filter(
        teacher=request.user
    ).annotate(
        test_count=Count('testresult')
    ).filter(test_count=0)

    activities = Activity.objects.filter(
        message__icontains=request.user.username
    ).order_by('-id')[:5]
    context = {

        'total': total_students,

        'avg_score': round(avg_score, 1),

        'latest_students': latest_students,

        'weak_students': weak_students,

        'upgrade_students': upgrade_students,

        'inactive_students': inactive_students,

        'activities': activities,
    }

    return render(
        request,
        'teacher_dashboard.html',
        context
    )


# =========================================
# STUDENT LIST
# =========================================

@login_required
def student_list(request):

    query = request.GET.get('q')

    students = Student.objects.filter(
        teacher=request.user
    )

    if query:

        students = students.filter(
            Q(name__icontains=query) |
            Q(student_class__icontains=query)
        )

    return render(
        request,
        'student_list.html',
        {
            'students': students
        }
    )


# =========================================
# ADD STUDENT
# =========================================

@login_required
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save(commit=False)

            student.teacher = request.user

            student.save()

            Activity.objects.create(
                message=f"{request.user.username} added {student.name}"
            )

            return redirect('student_list')

    else:

        form = StudentForm()

    return render(
        request,
        'add_student.html',
        {
            'form': form
        }
    )


# =========================================
# EDIT STUDENT
# =========================================

@login_required
def edit_student(request, id):

    student = get_object_or_404(
        Student,
        id=id,
        teacher=request.user
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            Activity.objects.create(
                message=f"{student.name} updated"
            )

            return redirect('student_list')

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'edit_student.html',
        {
            'form': form,
            'student': student
        }
    )


# =========================================
# DELETE STUDENT
# =========================================

@login_required
def delete_student(request, id):

    student = get_object_or_404(
        Student,
        id=id,
        teacher=request.user
    )

    Activity.objects.create(
        message=f"{student.name} deleted"
    )

    student.delete()

    return redirect('student_list')


# =========================================
# START QUIZ
# =========================================

@login_required
def start_learning(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id,
        teacher=request.user
    )

    questions = list(
        Question.objects.all()
    )

    random.shuffle(questions)

    questions = questions[:5]

    request.session['quiz'] = [
        q.id for q in questions
    ]

    request.session['current'] = 0

    request.session['score'] = 0

    return redirect(
        'quiz_question',
        student_id=student.id
    )


# =========================================
# SHOW QUESTION
# =========================================

@login_required
def quiz_question(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id,
        teacher=request.user
    )

    q_ids = request.session.get(
        'quiz',
        []
    )

    index = request.session.get(
        'current',
        0
    )

    if index >= len(q_ids):

        return redirect(
            'submit_test',
            student_id=student.id
        )

    question = Question.objects.get(
        id=q_ids[index]
    )

    return render(
        request,
        'learning_game.html',
        {
            'student': student,
            'question': question,
            'index': index + 1,
            'total': len(q_ids)
        }
    )


# =========================================
# SUBMIT ANSWER
# =========================================

@login_required
def submit_test(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id,
        teacher=request.user
    )

    q_ids = request.session.get(
        'quiz',
        []
    )

    index = request.session.get(
        'current',
        0
    )

    score = request.session.get(
        'score',
        0
    )

    if request.method == "POST":

        selected = request.POST.get(
            'answer'
        )

        q_id = request.POST.get(
            'question_id'
        )

        question = Question.objects.get(
            id=q_id
        )

        if selected == question.correct_answer:

            score += 1

        request.session['score'] = score

        request.session['current'] = index + 1

    if request.session['current'] >= len(q_ids):

        total = len(q_ids)

        percentage = int(
            (score / total) * 100
        ) if total > 0 else 0

        student.last_score = percentage

        student.save()

        TestResult.objects.create(
            student=student,
            score=score,
            total=total,
            percentage=percentage
        )

        Activity.objects.create(
            message=f"{student.name} scored {percentage}%"
        )

        request.session['quiz'] = []

        request.session['current'] = 0

        request.session['score'] = 0

        return render(
            request,
            'progress.html',
            {
                'student': student,
                'score': score,
                'total': total,
                'percentage': percentage
            }
        )

    return redirect(
        'quiz_question',
        student_id=student.id
    )


# =========================================
# REPORT
# =========================================

@login_required
def report(request):

    students = Student.objects.filter(
        teacher=request.user
    )

    total_students = students.count()

    total_tests = TestResult.objects.filter(
        student__teacher=request.user
    ).count()

    class_avg = TestResult.objects.filter(
        student__teacher=request.user
    ).aggregate(
        avg=Avg("percentage")
    )["avg"] or 0

    highest_score = TestResult.objects.filter(
        student__teacher=request.user
    ).aggregate(
        max=Max("percentage")
    )["max"] or 0

    lowest_score = TestResult.objects.filter(
        student__teacher=request.user
    ).aggregate(
        min=Min("percentage")
    )["min"] or 0


    # TOP PERFORMER

    top_performer = TestResult.objects.filter(
        student__teacher=request.user
    ).order_by(
        '-percentage'
    ).first()


    # WEAK PERFORMER

    weak_performer = TestResult.objects.filter(
        student__teacher=request.user
    ).order_by(
        'percentage'
    ).first()


    # INDIVIDUAL STUDENT PROGRESS

    student_progress = []

    for student in students:

        tests = TestResult.objects.filter(
            student=student
        )

        total_given = tests.count()

        average = tests.aggregate(
            Avg('percentage')
        )['percentage__avg'] or 0

        best = tests.aggregate(
            Max('percentage')
        )['percentage__max'] or 0

        student_progress.append({

            'name': student.name,

            'tests': total_given,

            'average': round(average, 1),

            'best': best

        })


    context = {

        "total_students": total_students,

        "total_tests": total_tests,

        "class_avg": round(class_avg, 1),

        "highest_score": highest_score,

        "lowest_score": lowest_score,

        "top_performer": top_performer,

        "weak_performer": weak_performer,

        "student_progress": student_progress,
    }

    return render(
        request,
        "report.html",
        context
    )