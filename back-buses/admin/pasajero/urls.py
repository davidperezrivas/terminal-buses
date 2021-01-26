from rest_framework import routers

from .viewsets import PasajeroViewSet

router = routers.SimpleRouter()
router.register('pasajeros', PasajeroViewSet)

urlpatterns = router.urls