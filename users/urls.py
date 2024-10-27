# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('successfully_registered/', views.successfully_registered, name='successfully_registered'),
    path('successfully_logged_in/', views.successfully_logged_in, name='successfully_logged_in'),
    path('patient_entry/', views.patient_entry, name='patient_entry'),
    path('history/', views.history, name='history'),
    path('delete_patients/', views.delete_patients, name='delete_patients'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),


]