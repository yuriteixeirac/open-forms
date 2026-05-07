from rest_framework import serializers
from django.db import models


class Types(models.TextChoices):
    TEXT = 'text'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    NUMBER = 'number'


class QuestionSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        data = kwargs.get('data', {})

        if data is None:
            print('vtnc')

        type = data.get('type')
        if type in (Types.CHECKBOX, Types.RADIO,):
            self.fields['options'].required = True


    question = serializers.CharField()
    type = serializers.ChoiceField(choices=Types.choices, default=Types.TEXT)
    options = serializers.ListField(child=serializers.CharField(), required=False)


    def validate(self, attrs) -> dict:
        if attrs.get('type') in (Types.CHECKBOX, Types.RADIO):
            if not attrs.get('options', None):
                raise serializers.ValidationError({
                    'options': 'No options were passed.'
                })
        return attrs
