from rest_framework import serializers
from .models import Course,Content,Enrollment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course 
        fields=['id','title','image','description','price','duration','created_at','is_free','ratings']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields=['id','title','video','course']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=['id','user','course','created_at']


