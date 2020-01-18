from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from account.models import Member
from requestlist.models import DonationRequest, DonationAction, DonorEvaluation

class MyPageTV(TemplateView):
    template_name = 'mypage_receiver/mypage_Main.html'

class PwPageTV(TemplateView):
    template_name = 'mypage_receiver/pwcheck.html'

class PrivateTV(TemplateView):
    template_name = 'mypage_receiver/private_read.html'

def update(request, pk):
    if request.method =='POST':
        member = get_object_or_404(Member, user__id=pk)
        member.phone_number = request.POST.get('phone_number', '')
        member.url = request.POST.get('url', '')
        member.description = request.POST.get('description', '')
        member.save()
        user = request.user
        user.set_password(request.POST.get('password', ''))
        user.save()
        auth.login(request, user)
        return redirect("mypage_receiver:private")
    else:
        return render(request, 'mypage_receiver/private_update.html')

class MyRequestLV(ListView):
    template_name = 'mypage_receiver/1myrequest.html'

    def get_queryset(self):
        return DonationRequest.objects.filter(progress = '후원가능', receiver__user__id = self.request.user.id)

class ReservationsLV(ListView):
    template_name = 'mypage_receiver/2reservations.html'

    def get_queryset(self):
        return DonationAction.objects.filter(donationRequest__id = self.kwargs['pk'])

class DetailDV(DetailView):
    template_name = 'mypage_receiver/3detail.html'

    def get_queryset(self):
        return DonationAction.objects.filter(id = self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = DonationAction.objects.get(id = self.kwargs['pk'])
        evaluations = DonorEvaluation.objects.filter(donor__user__id = action.donor.user.id)
        actions = DonationAction.objects.filter(donor__user__id = action.donor.user.id, completed = '완료')
        context['awesome'] = sum([x.donationRequest.amount for x in actions])
        if len(evaluations) == 0:
            context['avg'] = 0
            return context
        else:
            temp = int(sum([x.starNumber for x in evaluations]) / len(evaluations) *10)
            avg = temp/10
            context['avg'] = avg
            return context

def approve(request, pk):
    if request.method == 'GET':
        actionA = DonationAction.objects.get(id=pk)
        actions = DonationAction.objects.filter(donationRequest__id=actionA.donationRequest.id)
        for action in actions:
            action.approval = "거절"
            action.save()
        actionA.approval = "승인"
        actionA.donationRequest.progress = "후원진행중"
        actionA.save()
        actionA.donationRequest.save()
        object_list = DonationAction.objects.filter(approval = "승인", completed = 'yet')
        return render(request, 'mypage_receiver/4inprogress.html', {'object_list':object_list})

class InProgressLV(ListView):
    template_name = 'mypage_receiver/4inprogress.html'

    def get_queryset(self):
        return DonationAction.objects.filter(approval="승인", completed='yet')


def evaluation_incomplete(request, pk):
    if request.method == "GET":
        object = DonationAction.objects.get(id=pk)
        object.completed = "중지"
        object.donationRequest.progress = "후원완료"
        object.save()
        object.donationRequest.save()
        return render(request, 'mypage_receiver/5evaluation.html', {'object': object})


def evaluation_complete(request, pk):
    if request.method == "GET":
        object = DonationAction.objects.get(id=pk)
        object.completed = "완료"
        object.donationRequest.progress = "후원완료"
        object.completeDate = timezone.now()
        object.donationRequest.save()
        object.save()
        return render(request, 'mypage_receiver/5evaluation.html', {'object': object})

def write_evaluation(request):
    if request.method == "POST":
        action = DonationAction.objects.get(id = request.POST.get('id', ''))
        evaluation = DonorEvaluation(donor = action.donor,
                                     donationAction = action,
                                     starNumber = request.POST.get('starNumber', ''),
                                     note = request.POST.get('note', ''))
        evaluation.save()
        object_lists = DonationAction.objects.filter(donationRequest__receiver__user__id = request.user.id)
        object_list = object_lists.exclude(completed = 'yet')
        return render(request, 'mypage_receiver/6donation_ended.html', {'object_list': object_list})

class EndedLV(ListView):
    template_name = 'mypage_receiver/6donation_ended.html'

    def get_queryset(self):
        object_lists = DonationAction.objects.filter(donationRequest__receiver__user__id=self.request.user.id)
        object_list = object_lists.exclude(completed='yet')
        return object_list


