from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.api.models import Submission, Survey
from apps.api.serializers import SubmissionInputSerializer, SubmissionOutputSerializer

"""
TODO:
    - SEPARAR EM FUNÇÕES MENORES;
    - CRIAR TESTES UNITÁRIOS;
    - CONECTAR AO FRONT-END;
"""


class SubmissionViews(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Submission.objects.all()     # type: ignore
    serializer_class = SubmissionOutputSerializer


    def post(self, request, survey_id: int | None = None):
        serializer = SubmissionInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # 1. VERIFICANDO SURVEY
        survey: Survey = get_object_or_404(Survey, pk=survey_id)

        """
        2. VERIFICANDO SE OS IDS BATEM
            - pega todos os ids das perguntas e respostas,
            alinha com o .sort() e verifica se a lista é
            idêntica, tirando a conclusão da validade do payload
        """
        submission_question_ids: list[str] = [a.get('question_id') for a in serializer.validated_data.get('answers')]
        survey_question_ids: list[str] = [q.get('id') for q in survey.questions]    # type: ignore

        submission_question_ids.sort()
        survey_question_ids.sort()

        if submission_question_ids != survey_question_ids:
            return Response({
                'error': 'Possible tampering with the formulary.'
            }, status=400)


        """
        3. VERIFICANDO OS TIPOS DOS CAMPOS
            - iterea por cada pergunta e resposta e
            verifica se o tipo do campo 'value' bate
            com o tipo esperado. se não, levanta uma
            exceção que é tratada retornando uma response
        """

        # answers sorted by id
        answers = sorted(serializer.validated_data.get('answers'), key=lambda a: a['question_id'])
        questions = sorted(survey.questions, key=lambda q: q['id'])     # type: ignore

        try:
            for q, a in zip(questions, answers):
                value = a.get('value')
                type = q.get('type')

                if value is None:
                    continue

                match type:
                    case 'text' | 'radio':
                        if not isinstance(value, str):
                            raise ValidationError('')
                    case 'checkbox':
                        if not isinstance(value, list):
                            raise ValidationError('')
                    case 'number':
                        if not isinstance(value, int):
                            raise ValidationError('')
        except ValidationError:
            return Response({
                'error': 'Didn\'t expect input type.',
                'question_id': q.get('id'),
                'expected_type': q.get('type')
            }, status=400)


        """
        4. VERIFICANDO SE ESCOLHAS BATEM COM OPÇÕES FORNECIDAS
            - itera sobre questões e respostas, checa o tipo
            da questão, verifica se o tipo da pergunta atual
            é multichoice (radio, checkbock) e itera sobre as
            respostas para checar se todas as respostas estão
            nas opções providenciadas.
        """
        try:
            for q, a in zip(questions, answers):
                if q.get('type') not in ('checkbox', 'radio',):
                    continue

                options: list[str] = sorted(q.get('options'))
                raw_value: list | str | int | None = a.get('value')

                if raw_value is None:
                    continue

                value = sorted(raw_value) if isinstance(raw_value, list) else raw_value

                if isinstance(value, str):
                    if value in options:
                        continue
                    raise ValidationError('Option was not provided by survey.')
                elif isinstance(value, list):
                    for choice in value:
                        if choice in options:
                            continue
                        raise ValidationError('Option was not provided by survey.')

        except ValidationError as e:
            return Response({
                'error': str(e)
            }, status=400)

        submission = Submission(
            owner=request.user,
            survey=survey,
            answers=serializer.validated_data.get('answers')
        )
        submission.save()

        return Response({
            'message': 'Submission received successfully.'
        }, status=201)
