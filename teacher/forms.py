from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            'name',
            'age',
            'student_class',
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter student name'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter age'
            }),

            'student_class': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter class'
            }),
        }