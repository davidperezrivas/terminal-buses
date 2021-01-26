from rest_framework import routers

from .viewsets import ChoferViewSet

router = routers.SimpleRouter()
router.register('choferes', ChoferViewSet)

urlpatterns = router.urls
