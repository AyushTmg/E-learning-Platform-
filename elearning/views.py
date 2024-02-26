from .models import Course 
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .serializers import (CourseSerializer,CourseDetailSerializer)




# ! Course View 
class CourseView(ListAPIView):
    queryset = Course.objects.all().select_related('user')
    serializer_class = CourseSerializer




# ! Course Detail View 
class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all().prefetch_related('course_part').prefetch_related('course_part__content')
    serializer_class = CourseDetailSerializer
    lookup_field='id'

    

