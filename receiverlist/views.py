import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from account.models import Member
from django.contrib.auth.models import User
from account.models import ReceiverLike

class ReceiverListLV(ListView):
    paginate_by = 10
    template_name = 'receiverlist/receiverlist.html'

    def get_queryset(self):
        return Member.objects.filter(user__is_staff = True)

#ajax코드.
@require_POST
def like_receiver(request):
    id = request.POST.get('id', '')
    result = True
    try:
        object_list = ReceiverLike.objects.filter(receiver__user__id = id)
        object = object_list.get(donor_id = request.user.id)
        result = False
    except:
        result = True

    if result:
        member = Member.objects.get(user__id = id)
        selection = ReceiverLike(donor_id = request.user.id, receiver = member)
        selection.save()

    context = {'result':result}
    return HttpResponse(json.dumps(context), content_type='application/json')

@require_POST
def search(request):##이제 좀 완벽하게 이해가 되는 느낌이다!!!
    receiver = Member.objects.filter(user__is_staff = True)
    object_list = receiver.filter(Q(ad_category__icontains=request.POST.get('target', ''))|
                                  Q(ad_detail__icontains=request.POST.get('target', ''))|
                                  Q(name__icontains=request.POST.get('target', '')))
    return render(request, 'receiverlist/receiverlist.html', {'object_list':object_list})
