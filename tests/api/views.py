from rest_framework import viewsets, permissions
from tests.models import Test, Question
from .serializers import TestSerializer, QuestionSerializer

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all().select_related('author')
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
