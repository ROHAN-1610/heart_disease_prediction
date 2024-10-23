from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15)
    dob=models.DateField(null=True,blank=True)
    hospital_name=models.CharField(blank = True,max_length = 100)