from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("doctor-appointments/", views.doctor_appointments, name="doctor_appointments"),
    path("my-appointments/", views.patient_appointments, name="patient_appointments"),
    path("appointment/<int:appointment_id>/<str:status>/", views.update_appointment_status, name="update_appointment_status"),
    path("cancel-appointment/<int:appointment_id>/", views.cancel_appointment, name="cancel_appointment"),
    
]





