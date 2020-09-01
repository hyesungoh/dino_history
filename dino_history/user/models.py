from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from datetime import date

# Create your models here.
class Student(AbstractUser):
    def __str__(self):
        return self.username
    b_date = models.DateField(default=date.today)
    phone_num = models.CharField(max_length=45)
    cor_num = models.IntegerField(default=0)
    dino_level = models.CharField(max_length=10)
    

class Problem(models.Model):
    p_title = models.CharField(max_length=45)
    p_content = models.TextField()
    answer = models.CharField(max_length=20)

class Example(models.Model):
    p_num = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="problem", default="")
    e1 = models.CharField(max_length=20)
    e2 = models.CharField(max_length=20)
    e3 = models.CharField(max_length=20)
    e4 = models.CharField(max_length=20)
