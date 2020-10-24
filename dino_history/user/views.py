
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Problem, Example, Correct, Wrong
from .forms import SigninForm, UserForm, ProblemForm, ExampleForm, ProblemMultiForm
from django.db.models import Q

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect

from random import randint # 레벨에 따른 이미지 랜덤으로 사용하기 위해

# Create your views here.
def mypage(request, name):
    exp_for_lv_up = [1, 5, 10, 20, 100]
    max = 47

    current_user = Student.objects.get(username = name)
    percent = current_user.cor_num * 100 // exp_for_lv_up[current_user.dino_level]
    gauge = percent * max // 100

    correct_problem = Correct.objects.filter(student = current_user)
    wrong_problem = Wrong.objects.filter(student = current_user)
    dino_url = dino_img(current_user.dino_level, current_user.dino_class)

    rank_dict = return_my_ranking(current_user)

    return render(request, 'user/mypage.html', {'u': current_user, 'exp_range': range(gauge),
    'correct_problem': correct_problem,
    'wrong_problem': wrong_problem,
    'dino_url': dino_url,
    'total': rank_dict['총'],
    'gh': rank_dict['근현대'],
    'chs': rank_dict['조선시대'],
    'sg': rank_dict['삼국시대'],
    'ss': rank_dict['선사시대']
    })

def return_my_ranking(current_user):
    total_list = Student.objects.all().order_by('-cor_num')
    total = list(total_list).index(current_user) + 1

    gh_list = Student.objects.all().order_by('-gh_num')
    gh = list(gh_list).index(current_user) + 1

    chs_list = Student.objects.all().order_by('-chs_num')
    chs = list(chs_list).index(current_user) + 1

    sg_list = Student.objects.all().order_by('-sg_num')
    sg = list(sg_list).index(current_user) + 1

    ss_list = Student.objects.all().order_by('-ss_num')
    ss = list(ss_list).index(current_user) + 1

    rank_dict = {}
    rank_dict['총'] = total
    rank_dict['근현대'] = gh
    rank_dict['조선시대'] = chs
    rank_dict['삼국시대'] = sg
    rank_dict['선사시대'] = ss

    return rank_dict

def return_ranking():
    total = Student.objects.all().order_by('-cor_num')[0:10]
    gh = Student.objects.all().order_by('-gh_num')[0:10]
    chs = Student.objects.all().order_by('-chs_num')[0:10]
    sg = Student.objects.all().order_by('-sg_num')[0:10]
    ss = Student.objects.all().order_by('-ss_num')[0:10]

    d = {}
    d['총'] = total
    d['근현대'] = gh
    d['조선시대'] = chs
    d['삼국시대'] = sg
    d['선사시대'] = ss

    return d

def ranking(request):
    # total = Student.objects.all().order_by('-cor_num')[0:10]
    rank_dict = return_ranking()
    total = rank_dict['총']
    gh = rank_dict['근현대']
    chs = rank_dict['조선시대']
    sg = rank_dict['삼국시대']
    ss = rank_dict['선사시대']

    if request.user.is_active:
        my_rank_dict = return_my_ranking(request.user)
        my_total = my_rank_dict['총']
        my_gh = my_rank_dict['근현대']
        my_chs = my_rank_dict['조선시대']
        my_sg = my_rank_dict['삼국시대']
        my_ss = my_rank_dict['선사시대']

        return render(request, 'user/ranking.html', {'total': total,
        'gh': gh, 'chs': chs, 'sg': sg, 'ss': ss,
        'my_total': my_total, 'my_gh': my_gh, 'my_chs': my_chs,
        'my_sg': my_sg, 'my_ss': my_ss})

    return render(request, 'user/ranking.html', {'total': total,
    'gh': gh, 'chs': chs, 'sg': sg, 'ss': ss})

def problem_detail(request, pk):
    if not request.user.is_active: # 로그인 안했을 때
        # error view로 에러메세지와 함께 보냄
        return error(request, "로그인을 해야 문제를 풀 수 있어용")

    p = Problem.objects.get(id=pk)
    return render(request, 'user/problem_detail.html', {'p': p})

def problem(request):
    if not request.user.is_active: # 로그인 안했을 때
        # error view로 에러메세지와 함께 보냄
        return error(request, "로그인을 해야 문제를 풀 수 있어용")

    current_user = request.user
    problem_list = []
    for _ in range(5):
        problem_list.append(random_problem_without_correct(current_user))

    return render(request, 'user/problem.html', {'p': problem_list})

def problem_search(request):
    if not request.user.is_active: # 로그인 안했을 때
        # error view로 에러메세지와 함께 보냄
        return error(request, "로그인을 해야 문제를 풀 수 있어용")
    name = request.GET["name"]
    problem_list = Problem.objects.filter(p_content__contains=name)[0:8]

    if len(problem_list) == 0:
        msg = str(name) + "이/가 들어간 문제는 없어용 ㅠ"
        return error(request, msg)
    return render(request, 'user/problem_search.html', {'name': name, 'p': problem_list})

def problem_era(request):
    if not request.user.is_active: # 로그인 안했을 때
        # error view로 에러메세지와 함께 보냄
        return error(request, "로그인을 해야 문제를 풀 수 있어용")

    era = request.GET["era"]
    problem_list = Problem.objects.filter(p_era__contains=era)[0:5]
    return render(request, 'user/problem.html', {'p': problem_list})


def random_problem_without_correct(user):
    max_id = len(Problem.objects.all())-1
    while True:
        pk = randint(1, max_id)
        temp_problem = Problem.objects.filter(pk=pk).first()

        try: # 푼 문제는 return을 안하기 위해
            Correct.objects.get(student=user, problem=pk)
        except: # 아직 안 푼 문제는 return
            if temp_problem:
                return temp_problem


def solve(request, pk):
    exp_for_lv_up = [1, 5, 10, 20, 100]

    if not request.user.is_active: # 로그인 안했을 때
        # error view로 에러메세지와 함께 보냄
        return error(request, "로그인을 해야 문제를 풀 수 있어용")

    if request.method == 'POST':
        current_user = Student.objects.get(id = request.user.id) # 현재 유저
        current_problem = Problem.objects.get(id=pk) # 현재 문제

        try: # 만약 푼 문제를 또 풀었다면?
            Correct.objects.get(student=current_user, problem=current_problem)
            return render(request, 'user/solve_test.html', {'p': current_problem, 'u': current_user})

        except:
            passing_answer = request.POST['example'] # 유저가 선택한 답

            # pk 문제의 정답과 사용자가 선택한 정답이 동일할 때 (문자열 비교)
            if current_problem.answer == passing_answer:
                try: # 틀렸다가 맞았으면 해당 Wrong 모델 삭제
                    Wrong.objects.get(student=current_user, problem=current_problem).delete()
                except:
                    pass

                current_user.cor_num += 1 # 현재 유저의 맞은 정답 수 + 1
                current_user.exp += 1

                if exp_for_lv_up[current_user.dino_level] <= current_user.exp:
                    current_user.dino_level += 1
                    current_user.exp = 0

                    # 레벨업 해서 2나 3일 때
                    if current_user.dino_level == 2 or current_user.dino_level == 3:
                        current_user.dino_class = randint(0, 2) # 이미지 분류를 위해 랜덤

                # 시대 구분하여 현재 유저의 점수에 추가
                if current_problem.p_era == '근현대':
                    current_user.gh_num += 1
                elif current_problem.p_era == '조선시대':
                    current_user.chs_num += 1
                elif current_problem.p_era == '삼국시대':
                    current_user.sg_num += 1
                elif current_problem.p_era == '선사시대':
                    current_user.ss_num += 1

                current_user.save() # 업데이트 사항을 저장

                c = Correct() # 유저와 맞은 문제의 관계를 저장하는 모델
                c.student = current_user
                c.problem = current_problem
                c.save()
                return correct(request, current_problem.id)
            else:
                try: # 틀렸는데 또 틀리면 생성 안함
                    Wrong.objects.get(student=current_user, problem=current_problem)
                    return wrong(request, current_problem.id)
                except:
                    w = Wrong() # 유저와 틀린 문제의 관계를 저장하는 모델
                    w.student = current_user
                    w.problem = current_problem
                    w.save()
                    return wrong(request, current_problem.id)


        # return render(request, 'user/solve_test.html', {'p': current_problem, 'ans': passing_answer, 'u': current_user})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def correct(request, pk):
    return render(request, 'user/correct.html')

def wrong(request, pk):
    p = Problem.objects.get(id=pk)
    return render(request, 'user/wrong.html', {'p': p})



def anew(request):
    return render(request, 'user/anew.html')

def create(request):
    if request.user.id != 1:
        return redirect('main')

    if request.method == 'POST':
        form = ProblemMultiForm(request.POST)
        if form.is_valid():
            temp_problem = Problem()
            temp_problem.p_era = form['problem'].cleaned_data['p_era']
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

            return redirect('create')
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
            auth_login(request, user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패. 다시 시도하세요.")
    else:
        return render(request, 'user/login.html',{'signin_form': signin_form})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = Student.objects.create_user(username=form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'])
            # auth_login(request, new_user)
            return redirect('login')
        else:
            return error(request, 'Fail to Sign-Up')
    else:
        form = UserForm()
        return render(request, 'user/signup.html', {'form': form})


def Result_Search(request):
    return render(request, 'user/Result_Search.html')

def profile(request):
    return render(request, 'user/main.html')

def dino_img(level, cls):
    if level == 0 or level == 1:
        return level
    else:
        u = str(level) + '_' + str(cls)
        return u

def error(request, error_msg):
    return render(request, 'user/error.html', {'error_msg': error_msg})
