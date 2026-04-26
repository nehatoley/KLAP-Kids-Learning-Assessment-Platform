from django.db import models

class Detection(models.Model):
    image = models.ImageField(upload_to='detections/')
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)