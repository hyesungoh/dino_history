from django.shortcuts import render

# Create your views here.
def mypage(request):
    return render(request, 'user/mypage.html')

def ranking(request):
    return render(request, 'user/ranking.html')

def problem(request):
    return render(request, 'user/problem.html')

def aproblem(request):
    return render(requerst, 'user/aproblem.html')