from rest_framework.routers import DefaultRouter
from lists.api import ListsViewSetApi, ListsItemViewSetApi

router = DefaultRouter()
router.register(r'user', ListsViewSetApi)
router.register(r'', ListsItemViewSetApi)

urlpatterns = router.urls