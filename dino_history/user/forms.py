from django import forms
from .models import Student, Problem, Example
from betterforms.multiform import MultiModelForm

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['p_content', 'answer', 'p_era']

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['e1', 'e2', 'e3', 'e4']

class ProblemMultiForm(MultiModelForm):
    form_classes = {
        'problem' : ProblemForm,
        'example' : ExampleForm,
    }

class SigninForm(forms.ModelForm):
    class Meta:
        model = Student
        help_texts = {
            'username': None,
        }
        fields = ['username', 'password']

class UserForm(forms.ModelForm):
    class Meta:
        model = Student
        help_texts = {
            'username': None,
        }
        fields = ['username', 'password', 'email', 'phone_num']
