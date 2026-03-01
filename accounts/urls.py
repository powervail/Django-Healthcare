from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    
]





