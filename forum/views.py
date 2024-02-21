from .models import Question
from .serailizers import (
    QuestionSerailizer,
)


from rest_framework.viewsets import ModelViewSet



#! ViewSet For Question  
class QuestionViewSet(ModelViewSet):
    queryset=Question.objects.all().select_related('user')
    serializer_class=QuestionSerailizer
 
    def get_serializer_context(self):
        """
        For Passing User_id as serializer Context
        """
        user_id=self.request.user.id
        return {'user_id':user_id}
    


    


