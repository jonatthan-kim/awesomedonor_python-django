from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    phone_number = models.CharField(max_length=70)
    nickname = models.CharField(max_length=70, null=True, blank=True)#Donor
    category = models.CharField(max_length=70, null=True, blank=True)#Receiver
    ad_category = models.CharField(max_length=70, null=True, blank=True)#Receiver
    ad_detail = models.CharField(max_length=100, null=True, blank=True)#Receiver
    description = models.TextField(null=True, blank=True)# Receiver
    url = models.CharField(max_length=100, null=True, blank=True)  # Receiver

    def __str__(self):
        return self.name

class ReceiverLike(models.Model):
    donor_id = models.IntegerField()
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE)