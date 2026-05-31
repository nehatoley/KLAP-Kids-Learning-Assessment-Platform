from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

import random

from detection.models import (
    LearningLog,
    Question,
    UserAnswer
)

from user.decorators import role_required

from .models import Child
from .forms import ChildForm

from detection.models import QuizResult


# -------------------------
# PARENT DASHBOARD
# -------------------------

@login_required
@role_required('parent')
def parent_dashboard(request):

    children = Child.objects.filter(
        parent=request.user
    )

    for child in children:

        latest_answers = list(

            UserAnswer.objects.filter(
                child=child
            ).order_by('-id')[:10]

        )

        # Total Learned
        child.total_learned = sum(
            1 for a in latest_answers
            if a.is_correct
        )

        # Weak Areas
        weak_categories = set()

        for a in latest_answers:

            if not a.is_correct:
                weak_categories.add(
                    a.question.category.capitalize()
                )

        child.weak_areas = ", ".join(
            weak_categories
        ) if weak_categories else "None"

    return render(
        request,
        'parent_dashboard.html',
        {
            'children': children
        }
    )


# -------------------------
# ADD CHILD
# -------------------------

@login_required
@role_required('parent')
def add_child(request):

    form = ChildForm(
        request.POST or None
    )

    if form.is_valid():

        child = form.save(
            commit=False
        )

        # ✅ Current logged-in parent
        child.parent = request.user

        child.save()

        return redirect(
            'parent_dashboard'
        )

    return render(
        request,
        'add_child.html',
        {
            'form': form
        }
    )


# -------------------------
# CAMERA PAGE
# -------------------------

@login_required
@role_required('parent')
def parent_camera(request):

    children = Child.objects.filter(
        parent=request.user
    )

    return render(
        request,
        "camera.html",
        {
            "children": children,
            "mode": "parent"
        }
    )


# -------------------------
# LEARNING VIEW
# -------------------------

@login_required
@role_required('parent')
def learning_view(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
    )

    logs = LearningLog.objects.filter(
        child=child
    )

    objects = logs.values_list(
        'object_name',
        flat=True
    ).distinct()

    emoji_map = {

        "apple": "🍎",
        "banana": "🍌",
        "potato": "🥔",
        "dog": "🐶",
        "cat": "🐱",
        "car": "🚗"

    }

    data = []

    for obj in objects:

        emoji = emoji_map.get(
            obj.lower(),
            "📦"
        )

        data.append({

            "name": obj,
            "emoji": emoji

        })

    return render(
        request,
        'learning.html',
        {
            'child': child,
            'data': data
        }
    )


# -------------------------
# START QUIZ
# -------------------------

@login_required
@role_required('parent')
def start_quiz(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
    )

    questions = list(
        Question.objects.all()
    )

    random.shuffle(questions)

    questions = questions[:10]

    request.session['quiz'] = [
        q.id for q in questions
    ]

    request.session['current'] = 0

    request.session['answers'] = []

    return redirect(
        f'/parent/quiz/{child.id}/'
    )


# -------------------------
# SHOW QUESTION
# -------------------------

@login_required
@role_required('parent')
def quiz_question(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
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
            f'/parent/result/{child.id}/'
        )

    question = Question.objects.get(
        id=q_ids[index]
    )

    return render(
        request,
        'quiz.html',
        {
            'question': question,
            'index': index + 1,
            'child_id': child.id
        }
    )


# -------------------------
# SUBMIT ANSWER
# -------------------------

@login_required
@role_required('parent')
def submit_answer(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
    )

    if request.method == "POST":

        selected = request.POST.get(
            "answer"
        )

        q_id = request.POST.get(
            "question_id"
        )

        question = Question.objects.get(
            id=q_id
        )

        is_correct = (
            selected ==
            question.correct_answer
        )

        UserAnswer.objects.create(

            child=child,
            question=question,
            selected_answer=selected,
            is_correct=is_correct

        )

        answers = request.session.get(
            'answers',
            []
        )

        answers.append({

            'question_id': q_id,
            'is_correct': is_correct

        })

        request.session['answers'] = answers

        request.session['current'] += 1

    return redirect(
        f'/parent/quiz/{child.id}/'
    )


# -------------------------
# QUIZ RESULT
# -------------------------

@login_required
@role_required('parent')
def quiz_result(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
    )

    answers = request.session.get(
        'answers',
        []
    )

    total = len(answers)

    correct = sum(
        1 for a in answers
        if a['is_correct']
    )

    score = (
        (correct / total) * 100
    ) if total > 0 else 0


    QuizResult.objects.create(

        child=child,

        score=int(score),

        total_questions=total,

        correct_answers=correct

    )


    request.session['answers'] = []

    request.session['quiz'] = []

    request.session['current'] = 0


    return render(
        request,
        'result.html',
        {
            'child': child,
            'total': total,
            'correct': correct,
            'score': int(score)
        }
    )


# -------------------------
# SCORE VIEW
# -------------------------

@login_required
@role_required('parent')
def score_view(request, child_id):

    child = Child.objects.get(
        id=child_id,
        parent=request.user
    )

    results = QuizResult.objects.filter(
        child=child
    ).order_by('-created_at')

    total_quizzes = results.count()

    average_score = 0

    best_score = 0

    latest_score = 0

    if total_quizzes > 0:

        average_score = sum(
            r.score for r in results
        ) / total_quizzes

        best_score = max(
            r.score for r in results
        )

        latest_score = results.first().score

    return render(
        request,
        "scores.html",
        {
            "child": child,
            "results": results,
            "total_quizzes": total_quizzes,
            "average_score": int(average_score),
            "best_score": best_score,
            "latest_score": latest_score
        }
    )