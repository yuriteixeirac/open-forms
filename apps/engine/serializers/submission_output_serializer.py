from locale import str
from rest_framework import serializers
from .answer_serializer import AnswerSerializer


class SubmissionOutputSerializer(serializers.Serializer):
    owner = serializers.SerializerMethodField()
    survey_id = serializers.IntegerField()
    answers = serializers.ListField(child=AnswerSerializer())
    created_at = serializers.DateTimeField()


    def get_owner(self, instance) -> str:   # type: ignore
        return instance.owner.email
