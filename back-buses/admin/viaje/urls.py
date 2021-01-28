from rest_framework import routers

from .viewsets import ViajeViewSet

router = routers.SimpleRouter()
router.register('viajes', ViajeViewSet)

urlpatterns = router.urls
