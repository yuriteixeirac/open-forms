from rest_framework import serializers
from .answer_serializer import AnswerSerializer


class SubmissionInputSerializer(serializers.Serializer):
    survey_id = serializers.IntegerField()
    answers = serializers.ListField(child=AnswerSerializer())
