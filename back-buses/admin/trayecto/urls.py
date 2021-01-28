from rest_framework import routers

from .viewsets import TrayectoViewSet

router = routers.SimpleRouter()
router.register('trayectos', TrayectoViewSet)

urlpatterns = router.urls
