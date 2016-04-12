from rest_framework import routers

from .api import SiteAPIViewSet


router = routers.SimpleRouter()
router.register(r'sites', SiteAPIViewSet)

urlpatterns = router.urls
