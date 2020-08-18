from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'heritage/main.html')

def map(request):
    return render(request, 'heritage/map.html')
