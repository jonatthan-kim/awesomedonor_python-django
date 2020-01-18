import json
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .models import Member
from django.core.exceptions import ObjectDoesNotExist

# class MyPageTV(TemplateView):
#     template_name = "mypage.html"
def mypage(request):
    if request.method == 'GET':
        if request.user.is_staff:
            return redirect('mypage_receiver:main')
        else:
            return redirect('mypage_donor:main')

def register_donor(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get('username', ''),
            password=request.POST.get('password1', ''))
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        nickname = request.POST.get('nickname', '')
        Member(user=user, name=name, phone_number = phone_number, nickname = nickname).save()
        return redirect('account:login')
    else:
        return render(request, 'registration/register_donor.html')#여기에 변수를 추가해서 자바 스크립트를 작동시키는 건 나중에 해보기.

def register_receiver(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get('username', ''),
            password=request.POST.get('password1', ''),
            is_staff=True)
        name = request.POST.get('name', '')
        phone_number = request.POST.get('phone_number', '')
        category = request.POST.get('category', '')
        ad_category = request.POST.get('ad_category', '')
        ad_detail = request.POST.get('ad_detail', '')
        url = request.POST.get('url', '')
        Member(user=user, name=name, phone_number=phone_number, category=category,
               ad_category=ad_category, ad_detail=ad_detail, url=url).save()
        return redirect('account:login')
    else:
        return render(request, 'registration/register_receiver.html')

@require_POST
def checkID(request):
    username = request.POST.get('username', '')
    result = True
    try:
        user = Member.objects.get(user__username = username)
        result = False
    except:
        result = True
    context = {'result': result}
    return HttpResponse(json.dumps(context), content_type="application/json")

@require_POST
def checkpw(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')

    object = Member.objects.get(user__id=int(id))
    print(object.user.password)
    result = True
    if check_password(pw, object.user.password):
        result = True
    else:
        result = False
    context = {'result': result}
    return HttpResponse(json.dumps(context), content_type="application/json")