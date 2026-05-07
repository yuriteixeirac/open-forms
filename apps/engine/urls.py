from django.urls import path
from apps.engine.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'api/survey', SurveyViewSet, basename='survey')
router.register(r'api/submission', SubmissionViewSet, basename='submission')

urlpatterns = [
    path('survey/', survey_creation, name='survey-creation'),
]

urlpatterns += router.urls
