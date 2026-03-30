from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Appointment, Patient, Doctor


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = {
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
    }

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date']

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'gender', 'phone', 'address']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'phone','available_from', 'available_to']
        