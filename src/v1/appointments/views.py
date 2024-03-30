from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentListSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    filterset_fields = ['doctor', 'date']
    ordering_fields = ['date', 'time']
    permission_classes = [permissions.IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentSerializer
        return AppointmentListSerializer

    def create(self, request, *args, **kwargs):
        a = request.data
        a['user'] = request.user.id
        appointment = Appointment.objects.filter(time=request.data['time'], date=request.data['date'],
                                              doctor=request.data['doctor'])
        if appointment:
            return Response(
                {"error": "That time is not free."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=a)
        serializer.user = request.user.id
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        doctor = self.request.query_params.get('doctor')
        date = self.request.query_params.get('date')
        all_appointments = int(self.request.query_params.get('all'))
        if not all_appointments:
            queryset = queryset.filter(user=request.user.id)
        if doctor:
            queryset = queryset.filter(doctor=doctor)
        if date:
            queryset = queryset.filter(date=date)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_appointments(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return self.list(request)
