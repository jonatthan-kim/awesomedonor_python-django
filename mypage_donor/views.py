from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView, DetailView
from requestlist.models import DonationSelection, DonationRequest, DonationAction, DonorEvaluation
from account.models import ReceiverLike, Member

# Create your views here.
class MyPageTV(TemplateView):
    template_name = 'mypage_donor/mypage_Main.html'

class SelectionLV(ListView):
    template_name = 'mypage_donor/selection.html'
    model = DonationSelection

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservations'] = DonationAction.objects.filter(donor__user__id = self.request.user.id, approval = 'yet')
        return context

def deleteselection(request, pk):
    selection = get_object_or_404(DonationSelection, id = pk)
    selection.delete()
    return redirect('mypage_donor:selection')

def reservation(request):##https://kgu0724.tistory.com/105
    if request.method =='POST':
        id = request.POST.getlist('id', '')
        contactNumbers = request.POST.getlist('contactNumber', '')
        meetingDates = request.POST.getlist('meetingDate', '')
        donor = Member.objects.get(user__id = request.user.id)
        for i in range(len(id)):
            donationSelection = DonationSelection.objects.get(id = id[i])
            donationRequest = donationSelection.donationRequest
            number = contactNumbers[i]
            reservations= DonationAction(donor = donor, donationRequest = donationRequest, contactNumber = number, meetingDate = meetingDates[i])
            reservations.save()
            donationSelection.decided = True
            donationSelection.save()
        objects = DonationSelection.objects.filter(donor__user__id = request.user.id)
        reservations = DonationAction.objects.filter(donor__user__id = request.user.id, approval = 'yet')
        return render(request, 'mypage_donor/selection.html', {'object_list': objects, 'reservations': reservations,})
    else:
        return render(request, 'mypage_donor/selection.html')



class receiverLikeLV(ListView):
    template_name = 'mypage_donor/receiverLike.html'

    def get_queryset(self):
        return ReceiverLike.objects.filter(donor_id = self.request.user.id)

def deletereceiverlike(request, pk):
    like = get_object_or_404(ReceiverLike, id = pk)
    like.delete()
    return redirect('mypage_donor:receiverLike')

class PwPageTV(TemplateView):
    template_name = 'mypage_donor/pwcheck.html'

class PrivateTV(TemplateView):
    template_name = 'mypage_donor/private_read.html'

def update(request, pk):
    if request.method =='POST':
        member = get_object_or_404(Member, user__id=pk)
        member.nickname = request.POST.get('nickname', '')
        member.phone_number = request.POST.get('phone_number', '')
        member.save()
        user = request.user
        user.set_password(request.POST.get('password', ''))
        user.save()
        auth.login(request, user)
        return redirect("mypage_donor:private")
    else:
        return render(request, 'mypage_donor/private_update.html')

class InProgressLV(ListView):
    template_name = 'mypage_donor/donation_inprogress.html'

    def get_queryset(self):
        return DonationAction.objects.filter(donor__user__id = self.request.user.id, completed = 'yet', approval = '승인')

class SortbyNameLV(ListView):
    template_name = 'mypage_donor/donation_inprogress.html'

    def get_queryset(self):
        return DonationAction.objects.filter(donor__user__id=self.request.user.id, completed='yet', approval='승인').order_by("donationRequest__receiver__name", "meetingDate")

class SortbyDateLV(ListView):
    template_name = 'mypage_donor/donation_inprogress.html'

    def get_queryset(self):
        return DonationAction.objects.filter(donor__user__id=self.request.user.id, completed='yet', approval='승인').order_by("meetingDate", "donationRequest__receiver__name")

class CompleteLV(ListView):
    template_name = 'mypage_donor/donation_complete.html'

    def get_queryset(self):
        return DonationAction.objects.filter(donor__user__id=self.request.user.id, completed='완료').order_by("meetingDate", "donationRequest__receiver__name")
