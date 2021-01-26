from rest_framework import routers

from .viewsets import BusViewSet

router = routers.SimpleRouter()
router.register('buses', BusViewSet)

urlpatterns = router.urls
