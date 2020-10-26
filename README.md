# dino_history / 공아역
### 2020 멋쟁이 사자처럼 전체 해커톤 출품작
Front-end : 2명
Back-end : 2명
총 4명으로 진행된 프로젝트
Back-end로 참여했으며 문제 작성과 배포를 제외한 모든 부분에 참여
<hr>

## 프로젝트 소개
###### Django-version == 2.2.4
###### Python-version == 3.7.4


![공아역1](https://user-images.githubusercontent.com/26461307/97166080-00d83700-17c8-11eb-9cca-3e026e2deffc.jpg)



![공아역2](https://user-images.githubusercontent.com/26461307/97166088-03d32780-17c8-11eb-8d60-6853100e4dfd.jpg)

- 문제를 맞출 수록 exp가 늘며, 리스트로 관리되는 각 레벨업에 필요되는 exp에 충당될 시 레벨업되게 구현

  ```Python
  # user/views.py 196번 줄
  if exp_for_lv_up[current_user.dino_level] <= current_user.exp:
    current_user.dino_level += 1
    current_user.exp = 0

    # 레벨업 해서 2나 3일 때
    if current_user.dino_level == 2 or current_user.dino_level == 3:
        current_user.dino_class = randint(0, 2) # 이미지 분류를 위해 랜덤
  ```
  <br>
- `Student` Model에 레벨업 시 랜덤으로 클래스가 정해지며 공룡 이미지를 뿌려줄 때 각 레벨과 클래스에 맞는 이름으로 저장된 공룡 이미지 렌더링
  ```Python
  # user/views.py 335번 줄
  def dino_img(level, cls):
      if level == 0 or level == 1:
          return level
      else:
          u = str(level) + '_' + str(cls)
          return u
  ```
  <br>
- 프론트에서 제작해 준 경험치 바에 47개가 한 줄에 들어갈 수 있는 최대치이기에 아래와 같이 연산
  ```Python
    # user/views.py 15번 줄
    exp_for_lv_up = [1, 5, 10, 20, 100]
    max = 47

    current_user = Student.objects.get(username = name)
    percent = current_user.cor_num * 100 // exp_for_lv_up[current_user.dino_level]
    gauge = percent * max // 100
  ```
<br>

![공아역3](https://user-images.githubusercontent.com/26461307/97166096-07ff4500-17c8-11eb-8bb6-b241f8bef2ca.jpg)

- 시간관계상 문제들을 모아둔 txt 파일을 읽는 작업을 구현하지 못하고 만들어둔 `betterforms.multiform`을 사용한 crud 작업을 이용하여 문제를 추가

<br>

- Problem model과 Example model을 1대1 관계 설정, multiform을 이용한 값을 받아와 해당되는 값들을 할당하여 구현


  ``` Python
  # user/views.py 249번 줄
  temp_problem = Problem()
  temp_problem.p_era = form['problem'].cleaned_data['p_era']
  ...
  temp_problem.save()

  temp_example = Example()
  temp_example.p_num = temp_problem
  temp_example.e1 = form['example'].cleaned_data['e1']
  ...
  temp_example.save()
  ```


  <br>


- 문제를 풀었을 때는 문자열 값을 비교하여 연산
<br>
- 문제를 맞거나 틀렸을 때 관계형 모델을 이용하여 저장
  ``` Python
  # user/models.py 32
  class Correct(models.Model):
      student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="student", on_delete=models.CASCADE)
      problem = models.ForeignKey(Problem, related_name="c_problem", on_delete=models.CASCADE)

  class Wrong(models.Model):
      student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="who", on_delete=models.CASCADE)
      problem = models.ForeignKey(Problem, related_name="w_problem", on_delete=models.CASCADE)

  ```
  <br>


- 풀었는 데 또 풀었을 때 관계형 모델이 생산되거나 총 푼 문제 수가 늘면 안되며 틀렸는데 다시 풀었을 때 관계형 모델이 삭제 및 생성되야 한다.  `try`, `except`를 사용하여 objects.get하여 예외처리


<br>


- 문제 맞은, 틀린 사람과 그 비율은 views에서 render로 넘겨주지 않고 `Custom Template Filter`를 사용


<br>

![공아역4](https://user-images.githubusercontent.com/26461307/97166105-0a619f00-17c8-11eb-8b46-d341382e47ae.jpg)
- 지역 선택 및 검색 시에 문화재 정보를 보여줘야함


<br>


- 필요할 때 마다 문화재청 api를 호출하지 않고 모든 문화재 정보를 파싱하여 txt 파일로 저장 후 view에서 읽어 model object로 저장하는 연산을 수행


<br>


- [자세한 사항은 링크에 설명되어 있음](https://github.com/hyesungoh/Cultural_Heritage_Administration_API)


<br>


![공아역5](https://user-images.githubusercontent.com/26461307/97166118-0f265300-17c8-11eb-842d-3855fe7ee720.jpg)

- 전체 및 시대별 1위부터 10위까지를 반환하는 함수를 구현
  ```Python
  # user/views.py 64번 줄
  def return_ranking():
    total = Student.objects.all().order_by('-cor_num')[0:10]
    ...
    d = {}
    d['총'] = total
    ...

    return d
  ```
<br>

- 전체 및 시대별 로그인한 유저의 등수를 반환하는 함수를 구현

  ```python
  # user/views.py 39번 줄
  def return_my_ranking(current_user):
    total_list = Student.objects.all().order_by('-cor_num')
    total = list(total_list).index(current_user) + 1
    ...

    rank_dict = {}
    rank_dict['총'] = total
    ...

    return rank_dict
  ```

<hr>


## 프로젝트로 배운 점
1. MultiModelForm을 사용하여 두가지 모델의 정보를 입력받을 수 있는 form을 사용할 수 있다는 것을 알게 됨


```Python
# user/model.py
from betterforms.multiform import MultiModelForm

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['p_content', 'answer', 'p_era']

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = ['e1', 'e2', 'e3', 'e4']

class ProblemMultiForm(MultiModelForm):
    form_classes = {
        'problem' : ProblemForm,
        'example' : ExampleForm,
    }
```


<br>


- views에서 데이터를 읽을 때는 아래와 같이 사용 가능
```Python
if request.method == 'POST':
    form = ProblemMultiForm(request.POST)
    if form.is_valid():
        temp_problem = Problem()
        temp_problem.p_era = form['problem'].cleaned_data['p_era']
        ...
        temp_problem.save()

        temp_example = Example()
        temp_example.p_num = temp_problem
        temp_example.e1 = form['example'].cleaned_data['e1']
        ...
        temp_example.save()
```


<br>


2. Custom Template Filter를 사용하여 Template에 조금 더 자유롭고 가독성이 좋게 데이터를 보낼 수 있게 됨
```Python
# user/templatetags/problems_num.py
from django import template
# ..을 이용하여 현재 앱의 models.py를 import
from ..models import Correct, Wrong, Problem
register = template.Library()

# 문제 번호를 이용하여 문제를 푼 사람의 수를 반환
@register.simple_tag
def return_cor_num(problem_id):
    # try를 이용하여 예외처리
    try:
        problem = Problem.objects.get(id=problem_id)
        return Correct.objects.filter(problem=problem).count()
    except:
        return 0

# 문제 번호를 이용하여 문제를 시도한 사람의 수를 반환
@register.simple_tag
def return_tried_num(problem_id):
    # try를 이용하여 예외처리
    try:
        problem = Problem.objects.get(id=problem_id)
        tried_num = Correct.objects.filter(problem=problem).count()
        tried_num += Wrong.objects.filter(problem=problem).count()
        return tried_num
    except:
        return 0

# 맞은 사람, 시도한 사람, 두 정수를 이용하여 퍼센트 계산하여 반환
@register.simple_tag
def return_percent(correct, tried):
    # try를 이용하여 예외처리
    try:
        ans = correct * 100 // tried
        return ans
    except:
        return 0
```


<br>


- Template에서는 아래와 같이 사용

```Django
{% return_cor_num x.id as correct_people %}
<div class="item" id="items">{{ correct_people }}</div>
<hr class="hr1">
{% return_tried_num x.id as tried_people %}
<div class="item" id="items">{{ tried_people }}</div>
<hr class="hr1">
{% return_percent correct_people tried_people as percent %}
<div class="item" id="items">{{ percent }}%</div>
```


<hr>


## 더 배울 점
- 조금 더 클린한 코드 짜기
  - 함수명은 동사로
  - 코드 재사용률 높이기
  - 주석 다는 것 습관화하기
- Django CBV
- AWS deploy
- 협업을 위한 github 사용
- Frontend의 모든 것
