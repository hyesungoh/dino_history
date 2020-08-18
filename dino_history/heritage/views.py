from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'heritage/main.html')

def map(request):
    return render(request, 'heritage/map.html')

def signin(request):
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
        return render(request, 'insta/signin.html',{'signin_form': signin_form})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'],
            email = form.cleaned_data['email'],
            password = form.cleaned_data['password'])
            nickname = form.cleaned_data['nickname'],
            login(request, new_user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'insta/signup.html', {'form': form})