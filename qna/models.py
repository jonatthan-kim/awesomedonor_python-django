from django.db import models
from account.models import Member

class QnA(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    count = models.IntegerField(default=0)
    writeDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-writeDate',)

class QnAComment(models.Model):
    qna = models.ForeignKey(QnA, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField()
    writeDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-writeDate',)
