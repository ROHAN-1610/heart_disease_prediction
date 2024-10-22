from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.forms import AuthenticationForm

def home_page(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('successfully_registered')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('successfully_logged_in')
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid form input.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def successfully_registered(request):
    return render(request, 'users/successfully_registered.html')

def successfully_logged_in(request):
    return render(request, 'users/successfully_logged_in.html')
