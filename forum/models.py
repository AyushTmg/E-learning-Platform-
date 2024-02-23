from django.db import models
from django.conf import settings



# ! Models For Raising Question In The Forum
class Question(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=200)
    time_stamp=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='question')
    likes=models.IntegerField(default=0,null=True,blank=True)


    def __str__(self) -> str:
        """
        Retruns String Format For Question Module
        """
        return self.title
    



# ! Models For Answering Forums Questions 
class Answer(models.Model):
    description=models.CharField(max_length=100)
    time_stamp=models.DateTimeField(auto_now_add=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answer')
    likes=models.IntegerField(default=0,null=True,blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='answer')




# !Like  Model Answer
class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'user')




# !Like  Model Question
class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question', 'user')



