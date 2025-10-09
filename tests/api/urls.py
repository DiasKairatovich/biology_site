from rest_framework.routers import DefaultRouter
from .views import TestViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = router.urls
