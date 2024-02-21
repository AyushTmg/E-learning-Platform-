from rest_framework.response import Response
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import (IsAdminUser,IsAuthenticated,AllowAny)
from .serializers import ( ContentSerializer,CourseSerializer,EnrollmentSerializer )
from .models import ( Content , Course , Enrollment )
from rest_framework.status import HTTP_200_OK,HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet

class CourseView(ListAPIView):
    queryset = Course.objects.all().select_related('user')
    serializer_class = CourseSerializer

    def list(self,request,*args, **kwargs) -> Response:
        queryset = self.get_queryset()  
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all().select_related('user')
    serializer_class = CourseSerializer
    lookup_field='id'

    def retrieve(self, request, *args, **kwargs)-> Response:
        instance=self.get_object()
        serializer=self.serializer_class(instance)
        other_courses=Course.objects.exclude(id=instance.id)
        other_serializer=self.serializer_class(other_courses,many=True)

        response_data={
            'course_detail':serializer.data,
            'other_courses':other_serializer.data
        }
        return Response(response_data)
    
class ContentView(ListAPIView):
    queryset=Content.objects.select_related('course')
    serializer_class=ContentSerializer

    def list(self, request, *args, **kwargs):
        course_id = self.kwargs['id']
        queryset = self.get_queryset().filter(course_id=course_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


    
class ContentDetailView(RetrieveAPIView):
    # queryset=Content.objects.select_related('course')
    serializer_class=ContentSerializer
    lookup_field = 'content_id'

    def retrieve(self, request, *args, **kwargs):
        # course_id = self.kwargs['id']
        id=self.kwargs['content_id']
        instance=self.get_object()
        serializer=self.serializer_class(instance)
        return Response(serializer.data) 

class EnrollmentViewSet(ModelViewSet):
    http_method_names=['get','head','options''delete']
    queryset=Enrollment.objects.all()
    serializer_class=EnrollmentSerializer
    # permission_classes=[IsAdminUser]

