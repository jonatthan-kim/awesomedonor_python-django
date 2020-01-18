from django.contrib import admin
from .models import QnA, QnAComment
# Register your models here.
admin.site.register(QnA)
admin.site.register(QnAComment)
