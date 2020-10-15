from django.contrib import admin

from .models import Problem, Student, Example, Correct, Wrong

# Register your models here.

admin.site.register(Student)
admin.site.register(Problem)
admin.site.register(Example)
admin.site.register(Correct)
admin.site.register(Wrong)
