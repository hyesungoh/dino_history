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
from django.urls import path

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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
