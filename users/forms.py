# This is users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient,Appointment

class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    phone_number=forms.CharField(max_length=15, required=True)
    dob=forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900,2100)))
    hospital_name = forms.CharField(required=True,max_length=100)
    



class Meta:
    model = User
    fields = ['username','email','phone_number','dob','hospital_name','password1','password2']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name','doctor_name', 'appointment_date', 'appointment_time', 'location']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }    


class PatientForm(forms.ModelForm):
    
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'symptoms']

class Health_Prediction_form(forms.Form):     
        
        height = forms.FloatField(
        label='Height (cm)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        weight = forms.FloatField(
        label='Weight (kg)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        temperature = forms.FloatField(
        label='Temperature (C)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        heart_rate = forms.FloatField(
        label='Heart_rate (C)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        cholestrol = forms.FloatField(
        label='Cholestrol (mg/dl)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        blood_sugar = forms.FloatField(
        label='Blood_Sugar  (mg/dl)',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        systolic = forms.FloatField(
        label='Systolic Pressure',
       widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        diastolic = forms.FloatField(
        label='Diastolic Pressure',        widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        existing_conditions = forms.ChoiceField(
        choices=[
            ('Diabetes', 'Diabetes'),
            ('Hypertension', 'Hypertension'),
            ('High cholestrol', 'High cholestrol'),
            ('Asthma', 'Asthma'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        family_history = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        label='Family History of Heart Disease',
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        smoking_status = forms.ChoiceField(
        choices=[
            ('Never', 'Never'),
            ('Former', 'Former'),
            ('Current', 'Current'),
    
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        lab_status = forms.ChoiceField(
        choices=[
            ('High Blood Sugar', 'High Blood Sugar'),
            ('High cholestrol', 'High cholestrol'),
            ('Low Iron', 'Low Iron'),
            ('Normal Test Results', 'Normal Test Results'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )
        symptom= forms.ChoiceField(
        choices=[
            ('chest pain', 'chest pain'),
            ('dizziness', 'dizziness'),
            ('fatigue', 'fatigue'),
            ('nausea', 'nausea'),
            ('palpitations', 'palpitations'),
            ('shortness of breath', 'shortness of breath'),

        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )