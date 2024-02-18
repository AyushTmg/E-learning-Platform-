from rest_framework_nested import routers
from .views import CourseView , CourseDetailView,EnrollmentViewSet,ContentView,ContentDetailView
from django.urls import path

router=routers.DefaultRouter()
router.register('enrollment',EnrollmentViewSet,basename='enrollment')
urlpatterns = [
    path('courses/',CourseView.as_view(),name='course'),
    path('courses/<str:id>/',CourseDetailView.as_view(),name='course-detail'),
    path('courses/<str:id>/content/',ContentView.as_view(),name='content'),
    path('courses/<str:id>/content/<str:content_id>/',ContentDetailView.as_view(),name='content'),

]

urlpatterns+=router.urls