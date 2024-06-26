from rest_framework import serializers
from .models import Appointment
from drf_spectacular.utils import extend_schema_field
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor', 'time', 'date', 'appointment_option']


class AppointmentListSerializer(serializers.ModelSerializer):
    TIME_CHOICES = (
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
    )

    is_taken = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'doctor', 'time',
                  'date', 'appointment_option', 'is_taken']

    @extend_schema_field(bool)
    def get_is_taken(self, obj):
        """
        Check if the time slot is taken for the given date.
        """
        taken_time_slots = Appointment.objects.filter(
            date=obj.date, doctor=obj.doctor).values_list('time', flat=True)
        available_time_slots = [
            choice[0] for choice in self.TIME_CHOICES if choice[0] not in taken_time_slots]
        return obj.time in available_time_slots


user_model = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = user_model
        fields = (
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name',
        )
