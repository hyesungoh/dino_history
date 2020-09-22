from django.contrib import admin

from .models import Problem, Student, Example

# Register your models here.

admin.site.register(Student)
admin.site.register(Problem)
admin.site.register(Example)