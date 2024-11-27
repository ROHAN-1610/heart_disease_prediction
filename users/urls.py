# This is users/urls.py
from django.urls import path
from . import views
from .views import CustomLogoutView, login_view, reset_password, download_patient_records

urlpatterns = [
    path('', views.choose_role, name='choose_role'),  # Root URL maps to choose_role view
    path('register/', views.register, name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),  
    path('home/', views.home, name='home'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('health_predictions/', views.health_predictions_result, name='health_predictions'),
    path('health_predictions_result/', views.health_predictions_result, name='health_predictions_result'),
    path('health_prediction/', views.health_prediction, name='health_prediction_form'),
    path('appointments/', views.appointments, name='appointments'),
    path('cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('reschedule/<int:appointment_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('reports/', views.reports, name='reports'),
    path('login/', views.login_view, name='login'),
    path('successfully_registered/', views.successfully_registered, name='successfully_registered'),
    path('successfully_logged_in/', views.successfully_logged_in, name='successfully_logged_in'),
    path('patient_entry/', views.patient_entry, name='patient_entry'),
    path('history/', views.history, name='history'),
    path('delete_patients/', views.delete_patients, name='delete_patients'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('download_records/<str:search_query>/<str:gender>/', views.download_patient_records, name='download_patient_records'),
    path('download_records/<str:search_query>/', views.download_patient_records, name='download_patient_records_no_gender'),

]