from django.db import models
from django.contrib.auth.models import User
from v1.appointments.models import Appointment

class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_account")


class DoctorAdvice(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    advice = models.CharField(max_length=255)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
