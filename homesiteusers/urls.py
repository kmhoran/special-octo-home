from rest_framework.routers import DefaultRouter
from homesiteusers.api import UserProfileViewSet

router = DefaultRouter()
router.register(r'', UserProfileViewSet)

urlpatterns = router.urls