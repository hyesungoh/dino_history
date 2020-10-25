from django.shortcuts import render
from .models import Heritage
from user.models import Student
# from django.contrib.staticfiles.templatetags.staticfiles import static
# from django.contrib.staticfiles.storage import staticfiles_storage
import os

# Create your views here.
def main(request):
    if request.user.is_authenticated:
        user_now = request.user
        dino_url = dino_img(user_now.dino_level, user_now.dino_class)
        rank_dict = return_my_ranking(user_now)
        return render(request, 'heritage/main.html', {'user_now': user_now,
        'dino_url': dino_url,
        'total': rank_dict['총'],
        'gh': rank_dict['근현대'],
        'chs': rank_dict['조선시대']
        })
    else:
        return render(request, 'heritage/main_nosigned.html')

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

def map(request):
    return render(request, 'heritage/map.html')

def result(request):
    name = request.GET["name"]
    # 검색창에 무언가를 썼을 때
    if name:
        # 문화재 모델의 이름 기준으로 무언가가 포함된 오브젝트들을 가지고 옴
        heritages = Heritage.objects.filter(name__contains=name)[0:7]

        if len(heritages) < 1:
            msg = str(name) + "이/가 들어간 문화재가 없어용 ㅜ"
            return error(request, msg)
    else:
        # 무언가를 안썼을 때 상위 10개만 가지고 옴
        heritages = Heritage.objects.all()[0:7]
    return render(request, 'heritage/result.html', {'name': name, 'heritages': heritages})

def error(request, error_msg):
    return render(request, 'user/error.html', {'error_msg': error_msg})

def map_result(request):
    location = request.GET["location"]

    if location:
        heritages = Heritage.objects.filter(location__contains=location)[0:7]
    else:
        heritages = Heritage.objects.all()[0:7]
    return render(request, 'heritage/map_result.html', {'location': location, 'heritages': heritages})


def save_heritage(request):
    # txt_file_url = static('heritage/txt/heritage.txt')
    # txt_file_url = staticfiles_storage.url('heritage/txt/heritage.txt')

    # 문화재명1, 위치_도 + 위치_시, 이미지, 내용, 시대, 경도, 위도
    if len(Heritage.objects.all()) > 10:
        pass
    else:
        # module_dir = os.path.dirname(__file__)
        # file_path = os.path.join(module_dir, '/Users/ohyeseong/Documents/django/dino_history/dino_history/heritage/heritage.txt')
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, 'heritage.txt')
        heritage_txt = open(file_path, 'r')

        while True:
            line = heritage_txt.readline()
            if not line: break

            this_heritage = eval(line)

            temp_heritage = Heritage()
            temp_heritage.name = this_heritage['문화재명1']
            temp_heritage.location = this_heritage['위치_도'] + this_heritage['위치_시']
            temp_heritage.dynasty = this_heritage['시대']
            temp_heritage.img_url = this_heritage['이미지']
            temp_heritage.content = this_heritage['내용']
            temp_heritage.longitude = this_heritage['경도']
            temp_heritage.latitude = this_heritage['위도']
            temp_heritage.save()

    return render(request, 'heritage/save_test.html')

def dino_img(level, cls):
    if level == 0 or level == 1:
        return level
    else:
        u = str(level) + '_' + str(cls)
        return u
