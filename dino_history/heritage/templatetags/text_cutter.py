from django import template
# 커스텀 템플릿 태그를 위해 생성
register = template.Library()

@register.simple_tag
def text_cutter(text):
    t = text.split('\n')
    ans = ""
    for s in t[0:4]:
        ans += s
    return ans
