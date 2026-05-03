from rest_framework import serializers
from .question_serializer import QuestionSerializer


class SurveyInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    questions = serializers.ListField(child=QuestionSerializer())
