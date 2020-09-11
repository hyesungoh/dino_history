from django import forms
from .models import Student, Problem, Example
from betterforms.multiform import MultiModelForm

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['p_title', 'p_content', 'answer']

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['e1', 'e2', 'e3', 'e4', 'p_num']

class ProblemMultiForm(MultiModelForm):
    form_classes = {
        'problem' : ProblemForm,
        'Example' : ExampleForm,
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
        fields = ['username', 'password', 'email', 'b_date', 'phone_num']

