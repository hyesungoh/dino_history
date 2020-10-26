from django import template
from ..models import Correct, Wrong, Problem
# 커스텀 템플릿 태그를 위해 생성
register = template.Library()

@register.simple_tag
def return_cor_num(problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
        return Correct.objects.filter(problem=problem).count()
    except:
        return 0
@register.simple_tag
def return_tried_num(problem_id):
    try:
        problem = Problem.objects.get(id=problem_id)
        tried_num = Correct.objects.filter(problem=problem).count()
        tried_num += Wrong.objects.filter(problem=problem).count()
        return tried_num
    except:
        return 0

@register.simple_tag
def return_percent(correct, tried):
    try:
        ans = correct * 100 // tried
        return ans
    except:
        return 0
