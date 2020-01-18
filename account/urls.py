from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    #로그인, 로그아웃.
    path('', include('django.contrib.auth.urls')),
    path('mypage/', views.mypage, name = "mypage"),
    path('register/donor', views.register_donor, name = "register_donor"),
    path('register/receiver', views.register_receiver, name = "register_receiver"),
    path('checkid', views.checkID, name="checkID"),
    path('checkpw/', views.checkpw, name='checkpw'),#개인정보 접근 이전에...

]