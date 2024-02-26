from .views import CourseView , CourseDetailView
from django.urls import path


urlpatterns = [
    path('courses/',CourseView.as_view(),name='course'),
    path('courses/<str:id>/',CourseDetailView.as_view(),name='course-detail'),
]

