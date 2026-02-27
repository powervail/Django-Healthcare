from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Patient, Doctor

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data.get("role")

            print("selected role:", role) # debug to print role

            if role == "patient":
                Patient.objects.create(user=user)
            elif role == "doctor":
                Doctor.objects.create(user=user)

            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form":form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form":form})

def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

