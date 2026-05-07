from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from uuid import uuid4
from apps.api.models import Survey
from apps.api.serializers import SurveyInputSerializer, SurveyOutputSerializer


class SurveyViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Survey.objects.all()     # type: ignore


    def list(self, request):
        user_surveys = self.queryset.filter(owner=request.user)
        return Response(
            SurveyOutputSerializer(
                user_surveys,
                many=True
            ).data,
            status=200
        )


    def retrieve(self, request, pk: int):
        survey = self.queryset.filter(pk=pk).first()
        return Response(SurveyOutputSerializer(survey).data, status=200)


    def create(self, request):
        serializer = SurveyInputSerializer(data=request.data)


        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            })

        questions = serializer.data.get('questions')

        for question in questions:
            question['id'] = str(uuid4())[:4]

        survey = Survey(
            owner=request.user,
            name=serializer.data.get('name'),
            description=serializer.data.get('description'),
            questions=serializer.data.get('questions'),
            valid_until=serializer.data.get('valid_until'),
        )
        survey.save()

        return Response({
            'message': 'Survey created successfully.'
        }, status=201)
