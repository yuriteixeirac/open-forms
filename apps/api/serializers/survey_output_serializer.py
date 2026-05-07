from rest_framework import serializers
from apps.api.models import Survey
from .question_serializer import QuestionSerializer

class SurveyOutputSerializer(serializers.ModelSerializer):
    questions = serializers.ListField(child=QuestionSerializer())


    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'questions', 'created_at', 'updated_at', 'valid_until']
