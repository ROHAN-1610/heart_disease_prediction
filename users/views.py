from django.shortcuts import render, redirect
from .forms import RegisterForm, PatientForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Patient

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
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

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