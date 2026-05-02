from apps.engine.views import SurveyViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'survey', SurveyViews)

urlpatterns = []
urlpatterns += router.urls
