from django.urls import path
from apps.engine.views import *

urlpatterns = [
    path('survey/', survey_creation, name='survey-creation'),
]
