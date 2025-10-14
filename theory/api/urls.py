from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, TopicViewSet

router = DefaultRouter()
router.register(r"sections", SectionViewSet)
router.register(r"topics", TopicViewSet)

urlpatterns = router.urls
