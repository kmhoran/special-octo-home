from rest_framework.routers import DefaultRouter
from lists.api import ListViewSet, ListItemViewSet

router = DefaultRouter()
router.register(r'', ListViewSet)
router.register(r'item', ListItemViewSet)

urlpatterns = router.urls