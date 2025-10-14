from rest_framework import serializers
from theory.models import Section, Topic
from tests.models import Test

class TopicSerializer(serializers.ModelSerializer):
    # Покажем только название теста, а не все вопросы
    test_title = serializers.CharField(source="test.title", read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "title",
            "content",
            "order",
            "section",
            "test",
            "test_title",
        ]


class SectionSerializer(serializers.ModelSerializer):
    # Включим темы раздела
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ["id", "title", "description", "topics"]
