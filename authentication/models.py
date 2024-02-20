from django.db import models


from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin



# ! Custome User Model 
class User(AbstractBaseUser,PermissionsMixin):
    first_name=models.CharField(max_length=150)
    last_name=models.CharField(max_length=150)
    username=models.CharField(unique=True,max_length=150)
    email=models.EmailField(unique=True)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    # ! Assigning the Custom Manager
    objects=CustomUserManager()


    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)

    # ! Adding email as Username Field
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name','username']


    def __str__(self) -> str:
        """
        Returns a string representation of the user object.
        """
        return f"{self.username}"
    


