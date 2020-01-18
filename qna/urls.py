from django.urls import path, include
from . import views

app_name = 'qna'
urlpatterns = [
    path('', views.QnAListLV.as_view(), name = "main"),
    path('detail/<int:pk>/', views.QnADV.as_view(), name = "detail"),
    path('myqna/', views.MyQnALV.as_view(), name = 'myqna'),
    path('writeqna/', views.writeqna, name = 'writeqna'),
    path('writecomment/<int:pk>/', views.writecomment, name = 'writecomment'),
    path('update/<int:pk>/', views.update, name = 'update'),
    path('delete/<int:pk>/', views.delete, name='delete'),

]