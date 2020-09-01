"""dino_history URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

import heritage.views
import user.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # heritage_app
    path('', heritage.views.main, name='main'),
    path('map/', heritage.views.map, name='map'),

    # user_app
    path('mypage/', user.views.mypage, name='mypage'),
    path('ranking/', user.views.ranking, name='ranking'),
    path('problem/', user.views.problem, name='problem'),
<<<<<<< HEAD
    path('anew/create/', user.views.create, name='create'),
    path('update/<int:pk>', user.views.update, name='update'),
    path('delete/<int:pk>', user.views.delete, name='delete'),
=======
    path('Result_Search/', user.views.Result_Search, name='Result_Search'),

>>>>>>> 1470ae6d7daf2b3f668a65068c885b50ba89a73a
    path('login/', user.views.login, name='login'),
    path('signup/', user.views.signup, name='signup'),

    #social login test
     # 로그인
    path('account/', include('rest_auth.urls')),
    path('account/registration/', include('rest_auth.registration.urls')),
    path('account/', include('allauth.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

