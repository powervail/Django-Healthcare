from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=10, null=True,blank=True)
    phone = models.CharField(max_length=15, null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    def __str__(self):
        return f'Patient - {self.user.username}'
    

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, null=True,blank=True)
    phone = models.CharField(max_length=15, null=True,blank=True)
    available_from = models.TimeField(null=True,blank=True)
    available_to = models.TimeField(null=True,blank=True)

    def __str__(self):
        return f"Doctor - {self.user.username}"
    

class Appointment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.username} -> {self.doctor.user.username}"