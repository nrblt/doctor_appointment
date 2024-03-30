from rest_framework.routers import SimpleRouter

from .views import AppointmentViewSet

app_name = 'appointments'

router = SimpleRouter()
router.register("",AppointmentViewSet)
urlpatterns = router.urls
