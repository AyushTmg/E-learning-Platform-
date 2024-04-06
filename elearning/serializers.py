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

import cv2




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
    duration=serializers.SerializerMethodField(
        method_name='get_duration'
    )

    class Meta:
        model=Content
        fields=[
            'id',
            'title',
            'duration'
        ]


    def get_duration(self, content: Content):
        filename = content.video.path
        video = cv2.VideoCapture(filename)

        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        
        fps = video.get(cv2.CAP_PROP_FPS)

        duration_seconds = frame_count / fps

        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)

        seconds_str = "{:02d}".format(seconds)
        video.release()

        if minutes==0:
            return f"{seconds_str}s"
        
        return f"{minutes}m {seconds_str}s"




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

