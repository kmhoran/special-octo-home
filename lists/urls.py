from rest_framework.routers import DefaultRouter
from lists.api import ListViewSet, ListItemViewSet

router = DefaultRouter()
router.register(r'item', ListItemViewSet)
router.register(r'', ListViewSet)

urlpatterns = router.urls