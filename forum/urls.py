from rest_framework_nested import routers
from .views import (
    QuestionViewSet,
    AnswerViewSet
)


router=routers.DefaultRouter()
router.register('questions',QuestionViewSet,basename='question')

answer_router=routers.NestedDefaultRouter(router,'questions',lookup='question')
answer_router.register('answers',AnswerViewSet,basename='question-answer')


urlpatterns=router.urls+answer_router.urls