from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Problem, Example, Aproblem
from .forms import SigninForm, UserForm, CreateForm

from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
def mypage(request):
    return render(request, 'user/mypage.html')

def ranking(request):
    return render(request, 'user/ranking.html')

def problem(request):
    return render(request, 'user/problem.html')

def aproblem(request):
    aproblem = Aproblem.objects.all()
    return render(request, 'user/aproblem.html', {'aproblem':aproblem})

def anew(request):
    return render(request, 'user/anew.html')

def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aproblem')
    else:
        form = CreateForm()
        return render(request, 'user/anew.html', {'form':form})

def login(request):
    signin_form = SigninForm()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패. 다시 시도하세요.")
    else:
        return render(request, 'user/login.html',{'signin_form': signin_form})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'])
            b_date = form.cleaned_data['b_date'],
            login(request, new_user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'user/signup.html', {'form': form})
