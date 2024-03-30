from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Appointment(models.Model):
    TIME_CHOICES = (
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
    )

    APPOINTMENT_OPTIONS = (
        ('video_call', 'Video Call'),
        ('offline_meeting', 'Offline Meeting'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    time = models.CharField(max_length=5, choices=TIME_CHOICES)
    date = models.DateField()

    appointment_option = models.CharField(max_length=50, choices=APPOINTMENT_OPTIONS)

    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError("Appointment date should be in the future.")

        if self.date == timezone.now().date() and self.time < timezone.now().strftime('%H:%M'):
            raise ValidationError("Appointment time should be in the future.")

    def __str__(self):
        return f"Appointment for {self.user.username} with {self.doctor.username} at {self.time} on {self.date}"
