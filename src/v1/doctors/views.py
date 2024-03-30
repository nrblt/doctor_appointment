from django.http import JsonResponse
from v1.doctors.models import Doctor, DoctorAdvice
from v1.doctors.serializers import DoctorAdviceSerilizer
from v1.appointments.models import Appointment
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response


def get_doctors(request):
    doctors = Doctor.objects.all()

    # Creating a list to store the required fields for each doctor
    doctors_list = []
    for doctor in doctors:
        # Appending first_name and last_name of each doctor's user to the list
        doctors_list.append({
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
        })

    # Returning the data as JSON response
    return JsonResponse({'doctors': doctors_list})


class DoctorAdviceViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DoctorAdvice.objects.all()
    serializer_class = DoctorAdviceSerilizer

    def get_user(self):
        return self.request.user.id

    def create(self, request, *args, **kwargs):
        doctor = self.get_user()
        appointment = Appointment.objects.get(pk=request.data['appointment'])
        if appointment.doctor.id != doctor:
            return Response(
                {"error": "You can only create appointments for yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data
        data['doctor'] = self.get_user()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
