from rest_framework.routers import SimpleRouter

from v1.doctors.views import DoctorAdviceViewSet

app_name = 'doctors_advice'

router = SimpleRouter()
router.register("advice",DoctorAdviceViewSet)
urlpatterns = router.urls
