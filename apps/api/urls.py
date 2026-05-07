from apps.api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'survey', SurveyViewSet, basename='survey')
router.register(r'submission', SubmissionViewSet, basename='submission')

urlpatterns = []
urlpatterns += router.urls
