from rest_framework_nested import routers
from .views import CourseViewSet

router=routers.DefaultRouter()

router.register('courses',CourseViewSet,basename="courses")

urlpatterns = router.urls 