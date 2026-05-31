from django.db import models
from user.models import CustomUser


class Child(models.Model):

    parent = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='children',
        limit_choices_to={'role': 'parent'}
    )

    name = models.CharField(
        max_length=100
    )

    age = models.IntegerField()

    def __str__(self):

        return self.name