from rest_framework import serializers
from .models import Course,Content,Enrollment,CoursePart





class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course 
        fields=[
            'id',
            'title',
            'image',
            'description',
            'price',
            'duration',
            'time_stamp',
            'is_free',
        ]



class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields=[
            'id',
            'title',
            'video',
        ]


class CoursePartSerializer(serializers.ModelSerializer):
    content=ContentSerializer(many=True)
    class Meta: 
        model=CoursePart
        fields=[
            'id',
            'title',
            'content'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    course_part=CoursePartSerializer(many=True)
    class Meta:
        model=Course 
        fields=[
            'id',
            'title',
            'image',
            'description',
            'price',
            'duration',
            'time_stamp',
            'is_free',
            'course_part',
            
        ]







class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=[
            'id',
            'user',
            'course',
            'created_at'
        ]


