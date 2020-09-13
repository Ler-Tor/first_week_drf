from rest_framework import routers
from .views import RecipientViewSet, ProductSetsViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r'recipients', RecipientViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'product-sets', ProductSetsViewSet)
urlpatterns = router.urls
