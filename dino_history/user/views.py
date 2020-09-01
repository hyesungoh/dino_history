from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Problem, Example
from .forms import SigninForm, UserForm, ProblemForm

from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
def mypage(request):
    return render(request, 'user/mypage.html')

def ranking(request):
    return render(request, 'user/ranking.html')

def problem(request):
    problem = Problem.objects.all()
    return render(request, 'user/problem.html', {'problem':problem})

def anew(request):
    return render(request, 'user/anew.html')

def create(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem')
    else:
        form = ProblemForm()
        return render(request, 'user/anew.html', {'form':form})

def update(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('problem')
    else:
        form = ProblemForm(instance=problem)
        return render(request, 'user/anew.html', {'form': form})

def delete(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    problem.delete()
    return redirect('problem')

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

def Result_Search(request):
    return render(request, 'user/Result_Search.html')