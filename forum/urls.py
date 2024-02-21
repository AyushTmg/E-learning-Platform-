from rest_framework_nested import routers
from .views import QuestionViewSet


router=routers.DefaultRouter()
router.register('questions',QuestionViewSet,basename='question')


urlpatterns=router.urls