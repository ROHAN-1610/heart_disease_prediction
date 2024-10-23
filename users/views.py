from django.shortcuts import render,redirect
from.forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .models import Patient
from .forms import PatientForm
from django.http import HttpResponse
import csv
# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number=form.cleaned_data.get('phone_number')
            dob=form.cleaned_data.get('dob')
            hospital_name=form.cleaned_data.get('hospital_name')
            #saving phone numberand dob to the userprofile model
            profile = UserProfile(user=user,phone_number=phone_number,dob=dob,hospital_name=hospital_name)
            profile.save()
            login(request, user)
            return redirect('successfully_registered')  # This now matches the correct pattern name
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

def successfully_registered(request):
    return render(request, "users/successfully_registered.html")


def patient_entry(request):
    return render(request, 'users/patient_entry.html')

def login_view(request):  #dont name "login" bcoz django already have build-in log in function"
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('successfully_logged_in')  # Redirect successful login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required  # Ensure the user is logged in before accessing this view
def successfully_logged_in(request):
    return render(request, 'users/successfully_logged_in.html')

def patient_entry(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Save form data to the database
            return redirect('history')  # Redirect to history after saving
    else:
        form = PatientForm()
    
    return render(request, 'users/patient_entry.html', {'form': form})

# View for displaying the history of all registered patients
def history(request):
    patients = Patient.objects.all()  # Query to get all registered patients
    return render(request, 'users/history.html', {'patients': patients})