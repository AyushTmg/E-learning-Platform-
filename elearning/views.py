from utils.response.response import CustomResponse as cr
from .models import (
    Course,
    CourseOverView,
    WhoIsThisFor,
    WhatYouWillLearn,
    Prerequisite,
    CoursePart,
    Content
)


from .serializers import(
    CourseSerializer,
    CourseOverViewSerailizer,
    CoursePartSerailizer,
    PrerequisiteSerailizer,
    WhatYouWillLearnSerailizer,
    WhoIsThisForSerailizer
)


from rest_framework.viewsets import ModelViewSet



# ! Course ViewSet
class CourseViewSet(ModelViewSet):
    serializer_class=CourseSerializer
    queryset=Course.objects.all()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # !For Overview of the course
        course_overview=CourseOverView.objects.filter(
            course=instance
        )
        course_overview_serializer=CourseOverViewSerailizer(
            course_overview,
            many=True
        )

        # ! For showing the Course Part 
        course_part=CoursePart.objects.filter(
            course=instance
        ).prefetch_related('content')
        course_part_serailizer=CoursePartSerailizer(
            course_part,
            many=True
        )

        # ! For Showing what user will learn from this course
        learnings=WhatYouWillLearn.objects.get(
            course=instance
        )  
        what_you_will_learn_serailizer=WhatYouWillLearnSerailizer(
            learnings
        )

        # ! For showing the targeted audience for the course
        targeted_audience=WhoIsThisFor.objects.get(
            course=instance
        )
        who_is_this_for_serailizer=WhoIsThisForSerailizer(
            targeted_audience
        )


        # ! For pointing the prerequisite for the course
        prerequisite=Prerequisite.objects.get(
            course=instance
        )
        prerequisite_serailizer=PrerequisiteSerailizer(
            prerequisite
        )


        data={
            'course_detail':serializer.data,
            'course_overview':course_overview_serializer.data,
            'what_you_will_learn':what_you_will_learn_serailizer.data,
            'course_part':course_part_serailizer.data,
            'who_is_this_for':who_is_this_for_serailizer.data,
            'prerequisite':prerequisite_serailizer.data
        }

        return cr.success(
            data=data
        )






    

