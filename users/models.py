# This is users/models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=15)
    dob=models.DateField(null=True, blank=True)
    hospital_name=models.CharField(blank=True,max_length=100)


class Appointment(models.Model):
    patient_name = models.CharField(max_length=100, default="Unknown")
    doctor_name = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.doctor_name} - {self.appointment_date} at {self.appointment_time}"    


class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    symptoms = models.TextField()
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name