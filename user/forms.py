from django import forms

from django.contrib.auth.forms import (
    UserCreationForm
)

from .models import CustomUser


class UserRegistration(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = [

            "first_name",

            "last_name",

            "username",

            "email",

            "role",

            "password1",

            "password2"
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        #
        # 🔥 ALLOWED ROLES
        #
        self.fields["role"].choices = [

            ("teacher", "Teacher"),

            ("parent", "Parent")
        ]


class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField(
        widget=forms.PasswordInput()
    )
