from django.urls import path, include
from . import views

app_name = 'requestlist'
urlpatterns = [
    path('', views.RequestListLV.as_view(), name = "main"),
    path('filter/myrequest/', views.MyRequestLV.as_view(), name = "myrequest"),
    path('filter/receiver/<int:pk>/', views.FilterByReceiverLV.as_view(), name="FilterByReceiver"),
    path('filter/minorCategory/<str:name>/', views.FilterByMinCategoryLV.as_view(), name="FilterByMinCategory"),
    path('search/', views.search, name="search"),

    path('detail/<int:pk>/', views.RequestDV.as_view(), name="detail"),
    path('write/', views.writerequest, name="writerequest"),
    path('update/<int:pk>/', views.update, name = 'update'),
    path('delete/<int:pk>/', views.delete, name='delete'),

    path('select/', views.select_request, name='select_request'),

]