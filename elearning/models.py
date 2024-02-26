from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator, MaxValueValidator



# ! Course Model
class Course(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField()
    duration=models.IntegerField()
    image=models.ImageField(upload_to='course-images/')
    is_free = models.BooleanField(default=False)
    price = models.IntegerField(blank=True, null=True)
    time_stamp = models.DateField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def clean(self):
        if self.is_free:
            self.price = None  
        elif self.price is None:
            raise models.ValidationError("Price is required for non-free courses")
        

    def __str__(self) -> str:
        return self.title
    



# ! Course Part Model 
class CoursePart(models.Model):
    title=models.CharField(max_length=20)
    course=models.ForeignKey(Course, on_delete=models.CASCADE,related_name='course_part')

    def __str__(self) -> str:
        """
        For returing the string object of course part 
        """
        return self.title




# ! Content Model
class Content(models.Model):
    title=models.CharField(max_length=150)
    video=models.FileField( 
        upload_to='course-content/',validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mkv'])
        ])
    files=models.FileField(
        upload_to='content-file/',blank=True,null=True,validators=[
            FileExtensionValidator(allowed_extensions=["pdf", "docx"])
        ])
    course_part= models.ForeignKey(CoursePart, on_delete=models.CASCADE,related_name='content')

    
    def __str__(self) -> str:
        """
        For returing the string object of content
        """
        return self.title

    
    

# ! Enrollment Model 
class Enrollment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.PROTECT,related_name='enrollment')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='enrollment')
    time_stamp=models.DateField(auto_now_add=True) 


    def __str__(self) -> str:
        """
        For returning the string object of enrollment model
        """
        return f"{self.user} enrolled in {self.course} course"
