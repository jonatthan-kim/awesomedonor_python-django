from django.urls import path
from . import views

app_name = 'mypage_donor'
urlpatterns = [
    path('', views.MyPageTV.as_view(), name='main'),

    path('selection/<int:pk>/', views.SelectionLV.as_view(), name='selection'),
    path('selection/delete/<int:pk>/', views.deleteselection, name='delete_selection'),
    path('selection/reservation/', views.reservation, name='reservation'),

    path('receiverLike/', views.receiverLikeLV.as_view(), name='receiverLike'),
    path('receiverLike/delete/<int:pk>/', views.deletereceiverlike, name='delete_receiverlike'),

    path('pwpage/', views.PwPageTV.as_view(), name='pwpage'),
    path('private/', views.PrivateTV.as_view(), name='private'),
    path('private/update/<int:pk>/', views.update, name='update'),

    path('donation/inprogress', views.InProgressLV.as_view(), name='inprogress'),
    path('donation/inprogress/sortbyname/', views.SortbyNameLV.as_view(), name='sortbyname'),
    path('donation/inprogress/sortbydate/', views.SortbyDateLV.as_view(), name='sortbydate'),
    path('donation/complete/', views.CompleteLV.as_view(), name='complete'),

]