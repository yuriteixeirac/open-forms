from rest_framework import serializers

class ListOrStringOrIntegerField(serializers.Field):
    def to_internal_value(self, data):
        valid_types = [list, str, int]
        for type in valid_types:
            if isinstance(data, type):
                return data
            if data is None:
                return data
        self.fail('invalid')


    def to_representation(self, value):
        return value


class AnswerSerializer(serializers.Serializer):
    question_id = serializers.CharField()
    value = ListOrStringOrIntegerField()
