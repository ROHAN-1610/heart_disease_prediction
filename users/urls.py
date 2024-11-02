# This is users/urls.py
from django.urls import path
from . import views
from .views import CustomLogoutView, login_view, reset_password, download_patient_records

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
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