from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.api.views import *

router = DefaultRouter()

router.register(r'survey', SurveyViewSet, basename='api-survey')

urlpatterns = [
    path('submission/<int:pk>/', SubmissionViews.as_view(), name='submission-input'),
]

urlpatterns += router.urls
