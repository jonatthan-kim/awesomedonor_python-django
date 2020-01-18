"""awesomedonor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('mypage_donor/', include('mypage_donor.urls')),
    path('mypage_receiver/', include('mypage_receiver.urls')),
    path('receiverlist/', include('receiverlist.urls')),
    path('qna/', include('qna.urls')),
    path('requestlist/', include('requestlist.urls')),

    path('', views.HomeView.as_view(), name = "home"),
    path('intro/1/', views.Intro1TV.as_view(), name = "intro1"),
    path('intro/2/', views.Intro2TV.as_view(), name = "intro2"),
]
