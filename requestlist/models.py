from django.db import models
from account.models import Member
from django.core.validators import MaxValueValidator, MinValueValidator

class DonationRequest(models.Model):
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE)
    majorCategory = models.CharField(max_length=100)
    minorCategory = models.CharField(max_length=100)
    amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(50000)])
    writeDate = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    progress = models.CharField(max_length=20, default='후원가능')

    class Meta:
        ordering = ('-writeDate', )

class DonationSelection(models.Model):
    donor = models.ForeignKey(Member, on_delete=models.CASCADE)
    donationRequest = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    decided = models.BooleanField(default=False)

class DonationAction(models.Model):
    donor = models.ForeignKey(Member, on_delete=models.CASCADE)
    donationRequest = models.ForeignKey(DonationRequest, on_delete=models.CASCADE)
    contactNumber = models.CharField(max_length=70)
    meetingDate = models.DateField()
    completeDate = models.DateTimeField(blank=True, null=True)
    approval = models.CharField(max_length=20, default='yet')
    completed = models.CharField(max_length=20, default='yet')

    def __str__(self):
        return str(self.donationRequest.id) + "/"+ self.donor.name

    class Meta:
        ordering = ('id',)

class DonorEvaluation(models.Model):
    donor = models.ForeignKey(Member, on_delete=models.CASCADE)
    donationAction = models.ForeignKey(DonationAction, on_delete=models.CASCADE)
    starNumber = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-id',)