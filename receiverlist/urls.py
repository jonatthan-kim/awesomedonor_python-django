from django.urls import path
from . import views

app_name = 'receiverlist'
urlpatterns = [
    path('', views.ReceiverListLV.as_view(), name='main'),
    path('like/', views.like_receiver, name='like_receiver'),
    path('search/', views.search, name="search"),
]