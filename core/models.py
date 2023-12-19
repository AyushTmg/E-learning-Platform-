from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator
from django.conf import settings


class Course(models.Model):
    title=models.CharField(max_length=150)
    image=models.ImageField(upload_to='course-images/')
    description=models.TextField()
    duration=models.IntegerField()
    is_free = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ratings=models.IntegerField(
        validators=[
            MinValueValidator(1),MaxValueValidator(5)
        ])

    def clean(self):
        if self.is_free:
            self.price = None  
        elif self.price is None:
            raise models.ValidationError("Price is required for non-free courses")
        
    def __str__(self) -> str:
        return self.title
        
class Content(models.Model):
    title=models.CharField(max_length=150)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='content')
    video=models.FileField( 
        upload_to='course-content/',validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv'])
        ])
    files=models.FileField(
        upload_to='content-file/',blank=True,null=True,validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx"])
        ])
    
    def __str__(self) -> str:
        return self.title
    
    
    
class Enrollment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name='enrollment')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='enrollment')
    created_at=models.DateField(auto_now_add=True) 

    def __str__(self) -> str:
        return f"{self.user} enrolled in {self.course} course"
