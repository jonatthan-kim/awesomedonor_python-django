from django.urls import path
from . import views

app_name = 'mypage_receiver'
urlpatterns = [
    path('', views.MyPageTV.as_view(), name = 'main'),

    path('private/pwpage/', views.PwPageTV.as_view(), name='pwpage'),
    path('private/read/', views.PrivateTV.as_view(), name='private'),
    path('private/update/<int:pk>/', views.update, name='update'),##<int:pk>는 나중에 지워보기.

    path('donation/myrequest/', views.MyRequestLV.as_view(), name='myrequest'),
    path('donation/reservations/<int:pk>/', views.ReservationsLV.as_view(), name='reservations'),
    path('donation/detail/<int:pk>/', views.DetailDV.as_view(), name='reservations_detail'),
    path('donation/approve/<int:pk>/', views.approve, name='approve'),
    path('donation/inprogress/', views.InProgressLV.as_view(), name='inprogress'),
    path('donation/evaluation/incomplete/<int:pk>/', views.evaluation_incomplete, name='evaluation_incomplete'),
    path('donation/evaluation/complete/<int:pk>/', views.evaluation_complete, name='evaluation_complete'),
    path('donation/evaluation/write/', views.write_evaluation, name='write_evaluation'),
    path('donation/ended/', views.EndedLV.as_view(), name='ended'),

]