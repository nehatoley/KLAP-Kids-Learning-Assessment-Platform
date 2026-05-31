from django.contrib import admin
from .models import LearningLog, Question, UserAnswer

admin.site.register(LearningLog)
admin.site.register(Question)
admin.site.register(UserAnswer)