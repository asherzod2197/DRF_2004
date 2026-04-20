from rest_framework.routers import DefaultRouter
from .views import SotuvchiViewSet, MijozViewSet, QarzlarViewSet, TolovlarViewSet

router = DefaultRouter()
router.register(r'sotuvchilar', SotuvchiViewSet, basename='sotuvchi')
router.register(r'mijozlar', MijozViewSet, basename='mijoz')
router.register(r'qarzlar', QarzlarViewSet, basename='qarz')
router.register(r'tolovlar', TolovlarViewSet, basename='tolov')

urlpatterns = router.urls