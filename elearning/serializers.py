from rest_framework import serializers
from .models import Course,Content,Enrollment,CoursePart




# ! Serailizer For Course Model 
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




# ! Serailizer For Content Model 
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Content
        fields=[
            'id',
            'title',
            'video',
        ]




# ! Serailizer For Course Part Model
class CoursePartSerializer(serializers.ModelSerializer):
    content=ContentSerializer(many=True)
    class Meta: 
        model=CoursePart
        fields=[
            'id',
            'title',
            'content'
        ]




# ! Serailizer For Course Detail 
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




# ! Seraiilizer For Enrollment Model
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Enrollment
        fields=[
            'id',
        ]


    def create(self, validated_data):
        """
        Overrding create method for creating new enrollment instance 
        """
        course_id=self.context['course_id']
        user_id=self.context['user_id']
        return Enrollment.objects.create(
            course_id=course_id,
            user_id=user_id
        )


    


