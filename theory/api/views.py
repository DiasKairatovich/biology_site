from rest_framework import viewsets, permissions
from theory.models import Section, Topic
from .serializers import SectionSerializer, TopicSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.prefetch_related("topics").all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]  # потом можно заменить на IsAuthenticated


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.select_related("section", "test").all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]
