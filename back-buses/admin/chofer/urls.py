from rest_framework import routers

from .views import ChoferViews

router = routers.SimpleRouter()
router.register('choferes', ChoferViews)

urlpatterns = router.urls
