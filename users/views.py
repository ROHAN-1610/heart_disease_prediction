from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Patient
from django.contrib.auth import logout
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
import random,string

# Home view
def home(request):
    return render(request, 'home.html')

# Register view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            dob = form.cleaned_data.get('dob')
            hospital_name = form.cleaned_data.get('hospital_name')
            profile = UserProfile(user=user, phone_number=phone_number, dob=dob, hospital_name=hospital_name)
            profile.save()
            login(request, user)
            return redirect('successfully_registered')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

# View after successful registration
def successfully_registered(request):
    return render(request, "users/successfully_registered.html")

# Login view
def login_view(request):
    error_message = None  # Initialize error message
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('successfully_logged_in')
            else:
                error_message = "Invalid username or password."  # Set error message if authentication fails
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form, 'error_message': error_message})

# View after successful login
@login_required
def successfully_logged_in(request):
    return render(request, 'users/successfully_logged_in.html')

# View to register a new patient
@login_required
def patient_entry(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('history')
    else:
        form = PatientForm()
    return render(request, 'users/patient_entry.html', {'form': form})

# View to display patient history
@login_required
def history(request):
    if request.method == 'POST':
        # Get the list of patient IDs from the submitted form
        patient_ids = request.POST.getlist('patient_ids')  
        if patient_ids:  # Check if any IDs were selected
            Patient.objects.filter(id__in=patient_ids).delete()
            # Optionally add a success message here
            return redirect('history')  # Redirect after deletion

    # Retrieve all patients to display in the table
    patients = Patient.objects.all()
    return render(request, 'users/history.html', {'patients': patients})

# View to handle deletion of selected patients
@login_required
def delete_patients(request):
    if request.method == 'POST':
        patient_ids = request.POST.getlist('patient_ids')
        if patient_ids:
            Patient.objects.filter(id__in=patient_ids).delete()
    return redirect('history')

@login_required
def edit_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)  # Get the patient to be edited

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)  # Load form with patient instance data
        if form.is_valid():
            form.save()  # Save the updated patient details
            return redirect('history')  # Redirect to the history page after editing
    else:
        form = PatientForm(instance=patient)  # Load form with patient instance data

    return render(request, 'users/edit_patient.html', {'form': form, 'patient': patient})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))  # Redirect to the logout success page
    
def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)
                print(f"Resetting password for user: {username}")  # Debugging log
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')  # Redirect to the login page after reset
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                print("User does not exist")  # Debugging log
        else:
            messages.error(request, 'Passwords do not match. Please try again.')
            print("Passwords do not match")  # Debugging log

    return render(request, 'reset_password.html')