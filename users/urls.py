from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('home/', views.home, name='home'),
    path('choose-role/', views.choose_role, name='choose_role'),  # Map the choose_role view
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('health_predictions/form/', views.health_prediction, name='health_prediction_form'),
    path('health_predictions/result/', views.health_predictions_result, name='health_predictions_result'),
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
    path('logout/', views.user_logout, name='logout'),  # Add this line
    path('reset-password/', views.reset_password, name='reset_password'),
]
