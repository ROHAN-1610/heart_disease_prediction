# This is users/views.py
from django.shortcuts import render, redirect, get_object_or_404
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
import csv,pickle,random
import numpy as np
from django.http import HttpResponse
from .forms import Health_Prediction_form
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment
from .forms import AppointmentForm
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder



def choose_role(request):
    if request.method == "POST":
        selected_role = request.POST.get('role')  # Get the selected role
        if selected_role:
            request.session['user_role'] = selected_role  # Save role in session
            messages.success(request, f"Role '{selected_role}' selected successfully!")
            return redirect('home')  # Redirect to home after role selection
    return render(request, 'choose_role.html')  # Render the role selection page

def home(request):
    # Check if user role is selected
    if 'user_role' not in request.session:
        return redirect('choose_role')  # Redirect to choose_role view if no role is set

    # Render the home page
    return render(request, 'home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database

            # Generate OTP
            otp = random.randint(100000, 999999)  # OTP as a 6-digit number

            # Store OTP in session for verification
            request.session['otp'] = otp
            request.session['username'] = form.cleaned_data.get('username')
            request.session['password'] = form.cleaned_data.get('password1')

            # Send OTP via email
            subject = "Your OTP for Registration"
            message = f"Your OTP is: {otp}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [form.cleaned_data.get('email')]
            send_mail(subject, message, from_email, recipient_list)

            # Redirect to OTP verification page
            return redirect('verify_otp')
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def verify_otp(request):
    if request.method == "POST":
        otp_entered = request.POST.get('otp')

        # Check if OTP entered matches the stored OTP
        if otp_entered == str(request.session.get('otp')):
            # OTP is correct, log the user in
            username = request.session.get('username')
            password = request.session.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account successfully verified.')
                return redirect('login')  # Redirecting to login page after successful OTP verification
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'users/verify_otp.html')

def resend_otp(request):
    # Logic to resend OTP
    if request.method == "POST":
        # Example: Resend OTP logic here
        # Send an OTP to the user's registered phone or email
        return HttpResponse("OTP resent successfully.")
    
    # If accessed via GET, redirect or show a suitable message
    return redirect('verify_otp')  # Adjust based on your app logic


# View after successful registration
def successfully_registered(request):
    return render(request, "users/successfully_registered.html")

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the doctor_dashboard after successful login
            return redirect('doctor_dashboard')  # Assuming 'doctor_dashboard' is the correct URL name
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')  # You can display the error message in the login template

    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home') 

@login_required
def doctor_dashboard(request):
    # Any context or logic related to the doctor dashboard can be added here
    doctor_name = request.user.username  # For example, use the logged-in doctor's name
    return render(request, 'doctor_dashboard.html', {'doctor_name': doctor_name})

def view_patients(request):
    # Logic to retrieve patient data
    return render(request, 'view_patients.html')

def health_predictions_result(request):
    # You can handle the logic for showing the prediction result here
    return render(request, 'users/health_prediction_form.html')

def appointments(request):
    # Your logic to retrieve appointments
    return render(request, 'appointments.html')

# Cancel Appointment
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, 'Appointment canceled successfully.')
    return redirect('appointments')  # Redirect to the appointments page

# Reschedule Appointment
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        # Update the appointment details from the form
        appointment.appointment_date = request.POST.get('new_date')
        appointment.appointment_time = request.POST.get('new_time')
        appointment.save()
        messages.success(request, 'Appointment rescheduled successfully.')
        return redirect('appointments')  # Redirect to the appointments page
    return render(request, 'reschedule.html', {'appointment': appointment})  # Render a rescheduling form


def appointments(request):
    if request.method == "POST":
        # Handle form submission
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments')  # Redirect to the same page after saving the appointment
    else:
        # Display the form and existing appointments
        form = AppointmentForm()
        
    # Fetch all appointments from the database
    appointments_list = Appointment.objects.all()

    return render(request, 'appointments.html', {'form': form, 'appointments': appointments_list})


def reports(request):
    # Your logic to retrieve and display reports
    return render(request, 'reports.html') 

def manage_appointments(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments')
    else:
        form = AppointmentForm()

    # Fetch all appointments for the table
    appointments = Appointment.objects.all()
    return render(request, 'appointments.html', {'form': form, 'appointments': appointments})


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
    
# Logout view
def logout_view(request):
    logout(request)
    return redirect('login') 

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

# Load pre-trained models
# Health prediction logic
from django.http import JsonResponse
import pandas as pd
import joblib

# Load pre-trained models
def load_models():
    try:
        model = joblib.load(r'D:\python AC\heart_disease_prediction\heart_disease_prediction\knn_model.pkl')
        scaler = joblib.load(r'D:\python AC\heart_disease_prediction\heart_disease_prediction\scaler.pkl')
        one_hot_encoder = joblib.load(r'D:\python AC\heart_disease_prediction\heart_disease_prediction\encoder.pkl')
        label_encoder = joblib.load(r'D:\python AC\heart_disease_prediction\heart_disease_prediction\label_encoder.pkl')
        return model, scaler, one_hot_encoder, label_encoder
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None, None, None

def health_prediction(request):
    # Load models at the beginning
    model, scaler, one_hot_encoder, label_encoder = load_models()
    
    if not model:
        return JsonResponse({'error': 'Model loading failed'}, status=500)
    
    if request.method == 'POST':
        form = Health_Prediction_form(request.POST)
        if form.is_valid():
            # Capture the form data
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            temperature = form.cleaned_data['temperature']
            heart_rate = form.cleaned_data['heart_rate']
            cholestrol = form.cleaned_data['cholestrol']
            blood_sugar = form.cleaned_data['blood_sugar']
            systolic = form.cleaned_data['systolic']
            diastolic = form.cleaned_data['diastolic']
            existing_conditions = form.cleaned_data['existing_conditions']
            family_history = form.cleaned_data['family_history']
            smoking_status = form.cleaned_data['smoking_status']
            lab_status = form.cleaned_data['lab_status']
            symptoms = form.cleaned_data['symptom']
            
            categorical_columns = [
                'Symptoms_chest pain', 'Symptoms_dizziness', 'Symptoms_fatigue', 
                'Symptoms_nausea', 'Symptoms_palpitations', 'Symptoms_shortness of breath',
                'Existing_Conditions_Asthma', 'Existing_Conditions_Diabetes', 
                'Existing_Conditions_High Cholesterol', 'Existing_Conditions_Hypertension', 
                'Existing_Conditions_Thyroid', 'Laboratory_Test_Results_High Blood Sugar', 
                'Laboratory_Test_Results_High Cholesterol', 'Laboratory_Test_Results_Low Iron', 
                'Laboratory_Test_Results_Normal', 'Smoking_Status_Current', 
                'Smoking_Status_Former', 'Smoking_Status_Never', 
                'Family_History_Heart_Disease_No', 'Family_History_Heart_Disease_Yes'
            ]
            
            input_data = {col: [False] for col in categorical_columns}

            # Setting the appropriate columns to True based on user selection
            if 'chest pain' in symptoms:
                input_data['Symptoms_chest pain'] = [True]
            if 'dizziness' in symptoms:
                input_data['Symptoms_dizziness'] = [True]
            if 'fatigue' in symptoms:
                input_data['Symptoms_fatigue'] = [True]
            if 'nausea' in symptoms:
                input_data['Symptoms_nausea'] = [True]
            if 'palpitations' in symptoms:
                input_data['Symptoms_palpitations'] = [True]
            if 'shortness of breath' in symptoms:
                input_data['Symptoms_shortness of breath'] = [True]
            
            if 'Asthma' in existing_conditions:
                input_data['Existing_Conditions_Asthma'] = [True]
            if 'Diabetes' in existing_conditions:
                input_data['Existing_Conditions_Diabetes'] = [True]
            if 'High Cholesterol' in existing_conditions:
                input_data['Existing_Conditions_High Cholesterol'] = [True]
            if 'Hypertension' in existing_conditions:
                input_data['Existing_Conditions_Hypertension'] = [True]
            if 'Thyroid' in existing_conditions:
                input_data['Existing_Conditions_Thyroid'] = [True]
            
            if 'High Blood Sugar' in lab_status:
                input_data['Laboratory_Test_Results_High Blood Sugar'] = [True]
            if 'High Cholesterol' in lab_status:
                input_data['Laboratory_Test_Results_High Cholesterol'] = [True]
            if 'Low Iron' in lab_status:
                input_data['Laboratory_Test_Results_Low Iron'] = [True]
            if 'Normal' in lab_status:
                input_data['Laboratory_Test_Results_Normal'] = [True]
            
            if smoking_status == 'Current':
                input_data['Smoking_Status_Current'] = [True]
            if smoking_status == 'Former':
                input_data['Smoking_Status_Former'] = [True]
            if smoking_status == 'Never':
                input_data['Smoking_Status_Never'] = [True]
            
            if family_history == 'Yes':
                input_data['Family_History_Heart_Disease_Yes'] = [True]
            else:
                input_data['Family_History_Heart_Disease_No'] = [True]
            
            input_data['Height_cm'] = [height]
            input_data['Weight_kg'] = [weight]
            input_data['Temperature_C'] = [temperature]
            input_data['Heart_Rate'] = [heart_rate]
            input_data['Cholesterol_mg_dL'] = [cholestrol]
            input_data['Blood_Sugar_mg_dL'] = [blood_sugar]
            input_data['Systolic_BP'] = [systolic]
            input_data['Diastolic_BP'] = [diastolic]
            
            # Create DataFrame for the input data
            input_df = pd.DataFrame(input_data)
            
            # Define the columns order from the training data
            model_columns = [
                'Height_cm', 'Weight_kg', 'Temperature_C', 'Heart_Rate', 'Cholesterol_mg_dL', 
                'Blood_Sugar_mg_dL', 'Symptoms_chest pain', 'Symptoms_dizziness', 'Symptoms_fatigue', 
                'Symptoms_nausea', 'Symptoms_palpitations', 'Symptoms_shortness of breath',
                'Existing_Conditions_Asthma', 'Existing_Conditions_Diabetes', 
                'Existing_Conditions_High Cholesterol', 'Existing_Conditions_Hypertension', 
                'Existing_Conditions_Thyroid', 'Laboratory_Test_Results_High Blood Sugar', 
                'Laboratory_Test_Results_High Cholesterol', 'Laboratory_Test_Results_Low Iron', 
                'Laboratory_Test_Results_Normal', 'Smoking_Status_Current', 
                'Smoking_Status_Former', 'Smoking_Status_Never', 
                'Family_History_Heart_Disease_No', 'Family_History_Heart_Disease_Yes', 
                'Systolic_BP', 'Diastolic_BP'
            ]
            
            for col in model_columns:
                if col not in input_df.columns:
                    input_df[col] = 0  # Adding missing columns with value 0
            
            input_df = input_df[model_columns]

            # Make the prediction
            prediction = model.predict(input_df)
            
            # Get the disease name using label encoding 
            disease_name = label_encoder.inverse_transform(prediction)
            
            # Render the result page with the prediction
            return render(request, 'users/health_predictions_result.html', {'prediction': disease_name[0]})
        
        else:
            return JsonResponse({'error': 'Invalid form input'}, status=400)

    else:
        form = Health_Prediction_form()
        return render(request, 'users/health_prediction_form.html', {'form': form})