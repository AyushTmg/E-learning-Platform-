from .models import Question,Answer
from .permissions import IsUserObjectOrAdminPermission
from .serailizers import (
    QuestionSerailizer,
    AnswerSerailizer
)


from rest_framework.viewsets import ModelViewSet



#! ViewSet For Question  
class QuestionViewSet(ModelViewSet):
    queryset=(
        Question.objects
        .all()
        .select_related('user')
    )
    serializer_class=QuestionSerailizer 

    # ! For Specfying Method For ViewSet
    http_method_names=[
        'get',
        'options',
        'head',
        'post',
        'delete'
    ]

    # ! Custom Permission Called
    permission_classes=[IsUserObjectOrAdminPermission]
 

    def get_serializer_context(self):
        """
        For Passing User_id as serializer Context
        """
        user_id=self.request.user.id
        return {'user_id':user_id}
    


# ! ViewSet For Questions Answer
class AnswerViewSet(ModelViewSet):
    serializer_class=AnswerSerailizer

    # ! For Specfying Method For ViewSet
    http_method_names=[
        'get',
        'options',
        'head',
        'post',
        'delete'
    ]

    # ! Custom Permission Called
    permission_classes=[IsUserObjectOrAdminPermission]


    def get_queryset(self):
        """
        Overriding the queryset to filter the answer 
        by the question id present in the URL Parameter 
        """
        question_id=self.kwargs['question_pk']
        return (
            Answer.objects
            .filter(question_id=question_id)
            .select_related('user')
        )


    def get_serializer_context(self):
        """
        For Passing User_id as well as the questions 
        id as the context
        """
        user_id=self.request.user.id
        question_id=self.kwargs['question_pk']
        return {
            'user_id':user_id,
            'question_id':question_id
        }

    




