from django.contrib import admin
from .models import DonationRequest,DonationSelection,DonationAction, DonorEvaluation
# Register your models here.
admin.site.register(DonationRequest)
admin.site.register(DonationSelection)
admin.site.register(DonationAction)
admin.site.register(DonorEvaluation)

