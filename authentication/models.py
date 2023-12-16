from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    email=models.EmailField(unique=True)
    birth_date=models.DateField()

    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=CustomUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','birth_date']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile', primary_key=True)
    username=models.CharField(max_length=150,unique=True,null=True,blank=True)
    image=models.ImageField(upload_to='profile_image/',blank=True,null=True)
    phone=models.CharField(max_length=20, blank=True,null=True)
    bio=models.CharField(max_length=150, blank=True,null=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"


