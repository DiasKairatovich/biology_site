from rest_framework import serializers
from tests.models import Test, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "question_type",
            "option1", "option2", "option3", "option4",
            "image1", "image2", "image3", "image4",
            "correct_option",
            "correct_bool"
        ]

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ["id", "title", "description", "category", "author", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        test = Test.objects.create(**validated_data)
        for q_data in questions_data:
            Question.objects.create(test=test, **q_data)
        return test