from django.db import models

from django.contrib.auth.models import (
    AbstractUser
)


class CustomUser(AbstractUser):

    ROLE_CHOICES = [

        ("teacher", "Teacher"),

        ("parent", "Parent")
    ]

    role = models.CharField(

        max_length=20,

        choices=ROLE_CHOICES
    )

    def __str__(self):

        return self.username