from .models import (
    Course,
    CourseOverView,
    WhoIsThisFor,
    WhatYouWillLearn,
    Prerequisite,
    CoursePart,
    Content
)
from utils.exception.exception import CustomException as ce 

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer






# ! Course Serailizer 
class CourseSerializer(ModelSerializer):
    class Meta:
        model=Course
        fields=[
            'id',
            'title',
            'description',
            'duration',
            'image',
            'is_free',
            'price',
            'time_stamp',
        ]




# ! CourseOverView Serailizer
class CourseOverViewSerailizer(ModelSerializer):
    class Meta:
        model=CourseOverView
        fields=[
            'id',
            'title',
        ]




# ! WhoIsThisFor Serailizer
class WhoIsThisForSerailizer(ModelSerializer):
    class Meta:
        model=WhoIsThisFor
        fields=[
            'pk',
            'description'
        ]




# ! Prerequisite Serailizer
class PrerequisiteSerailizer(ModelSerializer):
    class Meta:
        model=Prerequisite
        fields=[
            'pk',
            'description'
        ]




# ! WhatYouWillLearn Serailizer
class WhatYouWillLearnSerailizer(ModelSerializer):
    class Meta:
        model=WhatYouWillLearn
        fields=[
            'pk',
            'description'
        ]



    
# ! Course Content Serailizer 
class ViewCourseContentSerailizer(ModelSerializer):

    class Meta:
        model=Content
        fields=[
            'id',
            'title',
        ]





# ! CoursePart Serializer 
class CoursePartSerailizer(ModelSerializer):
    content=ViewCourseContentSerailizer(
        many=True
    )
    
    class Meta:
        model=CoursePart
        fields=[
            'id',
            'title',
            'content'
        ]

