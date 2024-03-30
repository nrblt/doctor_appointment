from rest_framework import serializers
from v1.doctors.models import DoctorAdvice


class DoctorAdviceSerilizer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAdvice
        fields = '__all__'