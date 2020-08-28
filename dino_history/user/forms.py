from django import forms
from .models import Student, Aproblem

class CreateForm(forms.ModelForm):
    class Meta:
        model = Aproblem
        fields = ['a_title', 'a_content', 'a_answer']
        
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

