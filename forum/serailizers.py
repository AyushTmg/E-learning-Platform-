from .models import Question,Answer
from rest_framework import serializers 



# ! Serializer For Question 
class QuestionSerailizer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    class Meta:
        model=Question
        fields=[
            'id',
            'user',
            'title',
            'time_stamp',
            'description',
        ]


    def create(self, validated_data):
        """
        Overriding the create method to create a
        new question instance
        """
        user_id=self.context['user_id']
        return Question.objects.create(
            user_id=user_id,
            **validated_data
        )




# ! Serailizer For Question Answer
class AnswerSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=[
            'id',
            'user',
            'question',
            'time_stamp',
            'description',
        ]