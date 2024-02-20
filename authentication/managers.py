from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _ 


# ! Custom Manager For Custom User Model
class CustomUserManager(BaseUserManager):

    def create_user(self,email,password,**extra_fields):
        """
        Method Used for creating a normal user 
        """
        if not email:
            raise ValueError(_("email is a must"))
        
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user 
    
    def create_superuser(self,email,password,**extra_fields):
        """
        Method Used for creating a admin user 
        """
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser needs to have is_staff True"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser needs to have is_superuser True "))
        
        return self.create_user(email,password,**extra_fields)
    