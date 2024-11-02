# This is users/views.py
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
import csv
from django.http import HttpResponse

# Home view
def home(request):
    return render(request, 'home.html')

# Register view
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile(
                user=user,
                phone_number=form.cleaned_data.get('phone_number'),
                dob=form.cleaned_data.get('dob'),
                hospital_name=form.cleaned_data.get('hospital_name')
            )
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
    error_message = None
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
                error_message = "Invalid username or password."
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

# View to display patient history with search and filter options
@login_required
def history(request):
    search_query = request.GET.get('search', '')
    symptoms_query = request.GET.get('symptoms', '')
    gender_filter = request.GET.get('gender', '')

    # Initialize queryset
    patients = Patient.objects.all()

    # Filter by name if search_query is provided
    if search_query:
        patients = patients.filter(name__icontains=search_query)

    # Filter by symptoms if symptoms_query is provided
    if symptoms_query:
        patients = patients.filter(symptoms__icontains=symptoms_query)

    # Filter by gender if gender_filter is provided
    if gender_filter:
        patients = patients.filter(gender=gender_filter)

    context = {
        'patients': patients,
        'search_query': search_query,
        'symptoms_query': symptoms_query,
        'gender_filter': gender_filter,
    }
    return render(request, 'history.html', context)

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
    patient = Patient.objects.get(id=patient_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('history')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'users/edit_patient.html', {'form': form, 'patient': patient})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'reset_password.html')

def download_patient_records(request, search_query, gender=None):
    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="patient_records_{search_query}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patient ID', 'Name', 'Age', 'Gender', 'Symptoms', 'Registration Date'])

    # Filter patients based on the search query and optional gender
    if gender:
        patients = Patient.objects.filter(name__icontains=search_query, gender=gender)
    else:
        patients = Patient.objects.filter(name__icontains=search_query)

    # Write patient data to the CSV
    for patient in patients:
        writer.writerow([
            patient.id,
            patient.name,
            patient.age,
            patient.gender,
            patient.symptoms,
            patient.registration_date,
        ])

    return response