from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from datetime import date

# Create your models here.

class Problem(models.Model):
    def __str__(self):
        return self.p_title

    p_title = models.CharField(max_length=45)
    p_sort = models.CharField(max_length=20, null=True)
    p_content = models.TextField()
    answer = models.CharField(max_length=20)

class Student(AbstractUser):
    def __str__(self):
        return self.username
    b_date = models.DateField(default=date.today)
    phone_num = models.CharField(max_length=45)
    dino_level = models.IntegerField(default=0) # 공룡 레벨
    cor_num = models.IntegerField(default=0) # 맞은 문제의 수

class Correct(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="student", on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="c_problem", on_delete=models.CASCADE)

class Wrong(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="who", on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, related_name="w_problem", on_delete=models.CASCADE)

class Example(models.Model):
    p_num = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="problem", default="")
    e1 = models.CharField(max_length=20)
    e2 = models.CharField(max_length=20)
    e3 = models.CharField(max_length=20)
    e4 = models.CharField(max_length=20)
