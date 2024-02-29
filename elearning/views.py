from .models import Course ,Enrollment
from utils.response.response import CustomResponse as cr
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    EnrollmentSerializer,
)


from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)




# ! Course View 
class CourseView(ListAPIView):
    queryset = Course.objects.all().select_related('user')
    serializer_class = CourseSerializer 


    def list(self, request, *args, **kwargs):
        """
        Overrding the method just for adding custom response
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return cr.success(
            data=serializer.data
        )






# ! Course Detail View 
class CourseDetailView(RetrieveAPIView):
    queryset = Course
    serializer_class = CourseDetailSerializer
    lookup_field='id'


    def retrieve(self, request, *args, **kwargs):
        """
        Overrding the method just for adding custom response
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return cr.success(
            data=serializer.data,
        )
    



# ! Enrollment View 
class EnrollmentView(CreateAPIView):
    serializer_class=EnrollmentSerializer
    permission_classes=[IsAuthenticated]
    lookup_field='id'


    def get_serializer_context(self):
        """
        Method for passing course_id and user_id as
        context to serailizer
        """
        course_id=self.kwargs['id']
        user_id=self.request.user.id

        return {
            'course_id':course_id,
            'user_id':user_id
        }
    

    def create(self, request, *args, **kwargs):
        """
        Overrding the method just for adding custom response
        and adding valdiation for enrolling 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id=self.kwargs['id']
        course=Course.objects.get(id=course_id)

        if not course.is_free:
            return cr.error(message="You have to buy the course to enroll")    
 
        if Course.objects.filter(user=request.user, id=course_id).exists():
            return cr.error(message="Already Enrolled")
            
        self.perform_create(serializer)


        return cr.success(
            message="Successfully Enrolled",
            status=HTTP_201_CREATED
        )
    

    


    

    

