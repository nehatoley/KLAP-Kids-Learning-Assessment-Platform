from django.db import models
from parents.models import Child  # ✅ import from user app


# 📸 DETECTION (REAL-TIME RESULT)
class Detection(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='detections/')
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


# 🧠 LEARNING TRACK
class LearningLog(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    object_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    confidence = models.FloatField(null=True, blank=True)
    learned_at = models.DateTimeField(auto_now_add=True)


# ❓ QUESTION BANK
class Question(models.Model):

    QUESTION_TYPES = (
        ('text', 'Text Question'),
        ('image_question', 'Image Question'),
        ('image_option', 'Image Option'),
    )

    CATEGORY_CHOICES = (
        ('fruit', 'Fruit'),
        ('animal', 'Animal'),
        ('vegetable', 'Vegetable'),
    )

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='text'
    )

    question_text = models.CharField(max_length=255)

    # correct answer
    correct_answer = models.CharField(max_length=100)

    # text options
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)

    # images
    image = models.ImageField(upload_to='quiz/', null=True, blank=True)

    option1_image = models.ImageField(upload_to='quiz/', null=True, blank=True)
    option2_image = models.ImageField(upload_to='quiz/', null=True, blank=True)
    option3_image = models.ImageField(upload_to='quiz/', null=True, blank=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    difficulty = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text\


# 📝 USER ANSWERS
class UserAnswer(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    selected_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()

    answered_at = models.DateTimeField(auto_now_add=True)

class QuizResult(models.Model):

    child = models.ForeignKey(
        Child,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    total_questions = models.IntegerField()

    correct_answers = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.child.name} - {self.score}%"