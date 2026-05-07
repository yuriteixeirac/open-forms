from django.urls import path
from apps.engine.views import *

urlpatterns = [
    path('survey/', survey_creation, name='survey-creation'),
    path('survey/<int:pk>', survey_visualization, name='survey-visualization'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/survey/<int:pk>/', survey_detail, name='survey-detail')
]
