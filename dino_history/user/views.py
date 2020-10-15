from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Problem, Example, Correct, Wrong
from .forms import SigninForm, UserForm, ProblemForm, ExampleForm, ProblemMultiForm
from django.db.models import Q

from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
def mypage(request):
    return render(request, 'user/mypage.html')

def ranking(request):
    users = Student.objects.all().order_by('-cor_num')
    return render(request, 'user/ranking.html', {'users': users})

def problem(request):
    p = Problem.objects.all()
    return render(request, 'user/problem.html', {'p':p})

def solve(request, pk):
    if request.method == 'POST':
        current_user = Student.objects.get(id = request.user.id)
        current_problem = Problem.objects.get(id=pk)
        passing_answer = request.POST['example']

        # pk 문제의 정답과 사용자가 선택한 정답이 동일할 때 (문자열 비교)
        if current_problem.answer == passing_answer:
            current_user.cor_num += 1 # 현재 유저의 맞은 정답 수 + 1
            current_user.save() # 업데이트 사항을 저장

            c = Correct() # 유저와 맞은 문제의 관계를 저장하는 모델
            c.student = current_user
            c.problem = current_problem
            c.save()
        else:
            w = Wrong() # 유저와 틀린 문제의 관계를 저장하는 모델
            w.student = current_user
            w.problem = current_problem
            w.save()


        # return render(request, 'user/solve_test.html', {'p': current_problem, 'ans': passing_answer, 'u': current_user})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def anew(request):
    return render(request, 'user/anew.html')

def create(request):
    if request.method == 'POST':
        form = ProblemMultiForm(request.POST)
        if form.is_valid():
            temp_problem = Problem()
            temp_problem.p_title = form['problem'].cleaned_data['p_title']
            temp_problem.p_sort = form['problem'].cleaned_data['p_sort']
            temp_problem.p_content = form['problem'].cleaned_data['p_content']
            temp_problem.answer = form['problem'].cleaned_data['answer']
            temp_problem.save()

            temp_example = Example()
            temp_example.p_num = temp_problem
            temp_example.e1 = form['example'].cleaned_data['e1']
            temp_example.e2 = form['example'].cleaned_data['e2']
            temp_example.e3 = form['example'].cleaned_data['e3']
            temp_example.e4 = form['example'].cleaned_data['e4']
            temp_example.save()

            return redirect('problem')
    else:
        form = ProblemMultiForm()
        return render(request, 'user/anew.html', {'form':form})

 # answer에 있는 내용과 반복문 돌면서 e1~e4에 있는 내용이랑 일치하면 모달 띄우고 마이페이지 푼 문제에 저장


def update(request, pk): # 문제 업데이트
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == "POST":
        form = ProblemMultiForm(request.POST, instance=problem)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('problem')
    else:
        form = ProblemMultiForm(instance=problem)
        return render(request, 'user/anew.html', {'form': form})

def delete(request, pk): # 문제 삭제
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

def profile(request):
    return render(request, 'user/main.html')
