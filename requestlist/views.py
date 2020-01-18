import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import DonationRequest, DonationSelection
from account.models import Member

class RequestListLV(ListView):#
    model = DonationRequest
    template_name = 'requestlist/request_list.html'
    paginate_by = 10

class RequestDV(DetailView):#
    model = DonationRequest
    template_name = 'requestlist/request_detail.html'

class MyRequestLV(ListView):#
    template_name = 'requestlist/request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return DonationRequest.objects.filter(receiver__user__id = self.request.user.id)

class FilterByReceiverLV(ListView):
    template_name = 'requestlist/request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return DonationRequest.objects.filter(receiver__user__id = self.kwargs['pk'])

class FilterByMinCategoryLV(ListView):
    template_name = 'requestlist/request_list.html'
    paginate_by = 10

    def get_queryset(self):
        return DonationRequest.objects.filter(minorCategory__icontains = self.kwargs['name'])

@require_POST
def search(request):##이제 좀 완벽하게 이해가 되는 느낌이다!!!
    if request.POST.get('search' '')== 'both':
        object_list = DonationRequest.objects.filter(Q(receiver__ad_category__icontains=request.POST.get('target', ''))|
                                                  Q(receiver__ad_detail__icontains=request.POST.get('target', ''))|
                                                  Q(receiver__name__icontains=request.POST.get('target', '')))
        return render(request, 'requestlist/request_list.html', {'object_list':object_list})

    elif request.POST.get('search' '')== 'name':
        object_list = DonationRequest.objects.filter(Q(receiver__ad_category__icontains=request.POST.get('target', ''))|
                                                  Q(receiver__ad_detail__icontains=request.POST.get('target', '')))
        return render(request, 'requestlist/request_list.html', {'object_list': object_list})

    elif request.POST.get('search' '') == 'address':
        object_list = DonationRequest.objects.filter(receiver__name__icontains=request.POST.get('target', ''))
        return render(request, 'requestlist/request_list.html', {'object_list': object_list})

    else:
        object_list = DonationRequest.objects.filter(progress__icontains=request.POST.get('target', ''))
        return render(request, 'requestlist/request_list.html', {'object_list': object_list})

def writerequest(request):#
    if request.method =='POST':
        receiver = Member.objects.get(user__id=request.user.id)

        donrequest = DonationRequest(receiver=receiver,
                                     majorCategory=request.POST.get('majorCategory', ''),
                                     minorCategory=request.POST.get('minorCategory', ''),
                                     amount=request.POST.get('amount', ''),
                                     note=request.POST.get('note', ''),
                                     )
        donrequest.save()
        return redirect('requestlist:main')
    else:
        return render(request, 'requestlist/writerequest.html')

def update(request, pk):
    if request.method =='POST':
        object = get_object_or_404(DonationRequest, id=pk)
        object.majorCategory = request.POST.get('majorCategory', '')
        object.minorCategory = request.POST.get('minorCategory', '')
        object.amount = request.POST.get('amount', '')
        object.note = request.POST.get('note', '')
        object.save()
        return render(request, 'requestlist/request_detail.html', {'object':object})
    else:
        object = get_object_or_404(DonationRequest, id=pk)
        return render(request, 'requestlist/updaterequest.html', {'object':object})

def delete(request, pk):#
    qna = get_object_or_404(DonationRequest, id = pk)
    qna.delete()
    return redirect('requestlist:main')

##About selection
@require_POST
def select_request(request):
    id = request.POST.get('id', '')
    result = True
    try:
        object_list = DonationSelection.objects.filter(donationRequest__id = id)
        # if len(object_list)==0: 이게 0이면 아래 코드에서 100%에러가 나게 되어 있음!!.
        #     result = True
        object = object_list.get(donor__user__id = request.user.id)
        result = False
    except:
        result = True

    if result:
        requestList = DonationRequest.objects.get(id = id)
        selection = DonationSelection(donor = request.user.member, donationRequest = requestList)
        selection.save()

    context = {'result':result}
    return HttpResponse(json.dumps(context), content_type='application/json')
