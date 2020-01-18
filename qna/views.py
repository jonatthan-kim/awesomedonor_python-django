from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from qna.models import QnA, QnAComment
from account.models import Member

class QnAListLV(ListView):
    model = QnA
    paginate_by = 10

class QnADV(DetailView):

    def get_queryset(self):#이건 전달받은 객체의 '목록'이므로 단수는 불가능하고 오직 복수만 가능!!! 여기서 엄청 해맸음!!!
        qna = QnA.objects.filter(id = self.kwargs['pk'])#QnA.objects.get(id = self.request.GET.get('pk', ''))
        for i in qna:
            i.count += 1
            i.save()
        return qna


class MyQnALV(ListView):
    paginate_by = 10

    def get_queryset(self):
        return QnA.objects.filter(member__user__id = self.request.user.id)

def writeqna(request):
    if request.method == "POST":
        member = Member.objects.get(user__id = request.user.id)
        qna = QnA(member = member,
                  title=request.POST.get('title', ''),
                  content=request.POST.get('content', ''))
        qna.save()
        return redirect('qna:main')
    else:
        return render(request, 'QnA/writeqna.html')

def writecomment(request, pk):
    if request.method == 'POST':
        member = Member.objects.get(user__id=request.user.id)
        qna = QnA.objects.get(id = pk)
        comment = QnAComment(qna = qna,
                             member = member,
                             content = request.POST.get('content', ''))
        comment.save()
        return redirect('qna:main')

def update(request, pk):
    if request.method == 'POST':
        object = get_object_or_404(QnA, id=pk)
        object.title = request.POST.get('title', '')
        object.content = request.POST.get('content', '')
        object.save()
        return render(request, 'QnA/qna_detail.html', {'object': object})
    else:
        object = get_object_or_404(QnA, id=pk)
        return render(request, 'QnA/updateqna.html', {'object': object})

def delete(request, pk):
    qna = get_object_or_404(QnA, id = pk)
    qna.delete()
    return redirect('qna:main')
