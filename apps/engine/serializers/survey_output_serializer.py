from rest_framework import serializers
from apps.engine.models import Survey
from .question_serializer import QuestionSerializer

class SurveyOutputSerializer(serializers.ModelSerializer):
    schema = serializers.ListField(child=QuestionSerializer())


    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'schema', 'created_at', 'updated_at', 'valid_until']
