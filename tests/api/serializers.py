from rest_framework import serializers
from tests.models import Test, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'text', 'question_type',
            'option1', 'option2', 'option3', 'option4',
            'image1', 'image2', 'image3', 'image4',
            'correct_option', 'correct_bool',
        ]

class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'category', 'author', 'questions']
        read_only_fields = ['author']
