from .permissions import IsUserObjectOrAdminPermission
from .models import (
    Question,
    Answer,
    QuestionLike,
    AnswerLike
)

from .serailizers import (
    QuestionSerailizer,
    AnswerSerailizer,
    EmptySerializer
)


from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR
)


from django.shortcuts import get_object_or_404




#! ViewSet For Question  
class QuestionViewSet(ModelViewSet):
    queryset=(
        Question.objects
        .all()
        .select_related('user')
    )

    # ! Adding Filters Backend
    filter_backends=[SearchFilter,OrderingFilter]

    # ! Fields Used For Searching
    search_fields = ['title','description']

    #! Fields Used For Ordering
    ordering_fields=['time_stamp']
    

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


    def get_serializer_class(self):
        """
        Overriding the serailzer class for assigning Empty Serializer 
        the custom action name  like 
        """
        if self.action=='like':
            return EmptySerializer
        return QuestionSerailizer 


    def get_serializer_context(self):
        """
        For Passing User_id as serializer Context
        """
        user_id=self.request.user.id
        return {'user_id':user_id} 
    

    # ! Custom Like Action 
    @action(
            detail=True,
            methods=['POST','DELETE'],
            permission_classes=[IsAuthenticated]
        )
    def like(self,request,pk):
        """
        Custom Actions For Liking And Removing Like 
        From  Specific Question
        """
        user_id=request.user.id

        if request.method=='POST':
            try:
                # ! Create's a QuestionLike  Instance For The Question
                QuestionLike.objects.create(
                    user_id=user_id,
                    question_id=pk #! Used the question id received in the URL Parameter
                )
                
                # !Get the Question Instance  and Increase The Number Of Likes by One
                question=Question.objects.get(id=pk)
                question.likes+=1
                question.save()

                return Response(status=HTTP_201_CREATED)
        
            except Exception as e:
                # ! Just For handeling Expections
                print('Error alert: A user is trying to like same object multiple times ')
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        

        if request.method=='DELETE':
            # !  Get The Object That Is Being Deleted By Its ID
            question_like=get_object_or_404(
                QuestionLike,
                user_id=user_id,
                question_id=pk #! Used the question id received in the URL Parameter
            )
            # ! Delete The Like Instance
            question_like.delete()
 
            # !Get the Question Instance  and Decrease The Number Of Likes by One
            question=Question.objects.get(id=pk)
            question.likes-=1
            question.save()
            
            return Response(status=HTTP_204_NO_CONTENT)




# ! ViewSet For Questions Answer
class AnswerViewSet(ModelViewSet):

    # ! Adding Filters Backend
    filter_backends=[SearchFilter,OrderingFilter]

    #! Fields Used For Ordering
    ordering_fields=['time_stamp']

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


    def get_serializer_class(self):
        """
        Overriding the serailzer class for assigning Empty Serializer 
        the custom action name  like 
        """
        if self.action=='like':
            return EmptySerializer
        return AnswerSerailizer
    


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
    

    # ! Custom Like Action 
    @action(
            detail=True,
            methods=['POST','DELETE'],
            permission_classes=[IsAuthenticated]
        )
    def like(self,request,pk,question_pk):
        """
        Custom Actions For Liking And Removing Like 
        From  Specific Question
        """
        user_id=request.user.id

        if request.method=='POST':
            try:
                # ! Creates Answer Like Instance For The Answer
                AnswerLike.objects.create(
                    user_id=user_id,
                    answer_id=pk #! Used the answer id received in the URL Parameter
                )

                # ! Get the Answer Instance and Increase the no of likes by One
                answer=Answer.objects.get(id=pk)
                answer.likes+=1
                answer.save()

                return Response(status=HTTP_201_CREATED)
            
            except Exception as e:
                # ! Just For handeling Expections
                print('Error alert: A user is trying to like same object multiple times ')
                return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
        

        if request.method=='DELETE':
            # ! Get the Answer Like Instance If Exists Else Return Error 
            answer_like=get_object_or_404(
                AnswerLike,
                user_id=user_id,
                answer_id=pk #! Used the _like id received in the URL Parameter
            )
            # ! Deletes the answer like instance
            answer_like.delete()

            # ! Get the Answer Instance and decrease the no of likes by One 
            answer=Answer.objects.get(id=pk)
            answer.likes-=1
            answer.save()

            return Response(status=HTTP_204_NO_CONTENT)


    




