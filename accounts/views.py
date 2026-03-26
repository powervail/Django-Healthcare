from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AppointmentForm
from .models import Patient, Doctor,Appointment
from django.contrib import messages
from datetime import timedelta, datetime
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
    user = request.user

    if hasattr(user, "patient"):
        return redirect("patient_dashboard")
    elif hasattr(user, "doctor"):
        return redirect("doctor_dashboard")
    else:
        return redirect("login")
    

@login_required
def patient_dashboard(request):
    # Restrict Each Dashboard
    if not hasattr(request.user, 'patient'):
        return redirect("dashboard")
    return render(request,"accounts/patient_dashboard.html")

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, "doctor"):
        return redirect("dashboard")
    return render(request, "accounts/doctor_dashboard.html")

@login_required
def book_appointment(request):
    patient = Patient.objects.get(user=request.user)

    form = AppointmentForm(request.POST or None)

    slots = []
    
    if request.method == 'POST':

        if form.is_valid():
            appointment = form.save(commit=False)
            
            doctor = appointment.doctor
            date = appointment.appointment_date

            # Get selected slot from POST
            selected_time = request.POST.get("time_slot")

            if selected_time:
                selected_time = datetime.strptime(selected_time, "%H:%M").time()

                # Generated slots
                slots = generate_time_slots(
                    doctor.available_from,
                    doctor.available_to
                )

            # Check if selected is valid
            if selected_time not in slots:
                messages.error(request, "Invaild time slot")
                return redirect("book_appointment")
            

            
            # Prevent double booking
            exists = Appointment.objects.filter(doctor=doctor, appointment_date=appointment.appointment_date, appointment_time=selected_time).exists()

            if exists:
                messages.error(request, "This time slot is already booked")
                return redirect("book_appointment")
            
            # Save appointment
            appointment.patient = patient
            appointment.appointment_time = selected_time
            appointment.save()

            messages.success(request, "Appointment booked successfully")

            return redirect("patient_dashboard")
    
    # If doctor selected, generate slots
    if form.is_bound and form.is_valid():
        doctor = form.cleaned_data.get("doctor")
        if doctor:
            slots = generate_time_slots(
                doctor.available_form,
                doctor.available_to
            )

    return render(request, "accounts/book_appointment.html", {"form": form, "slots":slots})

@login_required
def doctor_appointments(request):
    doctor = Doctor.objects.get(user=request.user)

    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "accounts/doctor_appointments.html", {"appointments": appointments})

@login_required
def patient_appointments(request):
    patient = Patient.objects.get(user=request.user)

    appointments = Appointment.objects.filter(patient=patient)
    
    return render(request, "accounts/patient_appointments.html", {
        "appointments" : appointments
    })


@login_required
def cancel_appointment(request, appoointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_ide)

    # Security check: only owner can cancel
    if appointment.patient.user != request.user:
        return redirect("patient_dashboard")

    # Allow cancel only if pending
    if appointment.status == "pending":
        appointment.status ="cancelled"
        appointment.save()

    return redirect("patient_appointments")

def update_appointment_status(request, appointment_id, status):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    appointment.status = status
    appointment.save()

    return redirect("doctor_appiontments")

def generate_time_slots(start, end):
    slots = []
    current = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)

    while current <= end_time:
        slots.append(current.time())
        current += timedelta(minutes=30)

    return slots
