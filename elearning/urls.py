from django.urls import path
from .views import(
    CourseView,
    CourseDetailView,
    EnrollmentView
) 


urlpatterns = [
    path('courses/',CourseView.as_view(),name='course'),
    path('courses/<str:id>/',CourseDetailView.as_view(),name='course-detail'),
    path('courses/<str:id>/enroll/',EnrollmentView.as_view(),name='enroll'),
]

