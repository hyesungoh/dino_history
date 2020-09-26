from django.shortcuts import render
from .models import Heritage
# from django.contrib.staticfiles.templatetags.staticfiles import static
# from django.contrib.staticfiles.storage import staticfiles_storage
import os

# Create your views here.
def main(request):
    return render(request, 'heritage/main.html')

def map(request):
    return render(request, 'heritage/map.html')

def result(request):
    return render(request, 'heritage/result.html')

def save_heritage(request):
    # txt_file_url = static('heritage/txt/heritage.txt')
    # txt_file_url = staticfiles_storage.url('heritage/txt/heritage.txt')

    # 문화재명1, 위치_도 + 위치_시, 이미지, 내용, 시대, 경도, 위도
    if len(Heritage.objects.all()) > 10:
        pass
    else:
        module_dir = os.path.dirname(__file__)
        file_path = os.path.join(module_dir, '/Users/ohyeseong/Documents/django/dino_history/dino_history/heritage/heritage.txt')
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
