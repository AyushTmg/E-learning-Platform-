from .models import User 
from .tasks import password_reset_task,change_email_task

from rest_framework import serializers


from django.utils.translation import gettext_lazy as _ 
from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode




# ! Serializer For User Registration 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        write_only=True,
        style={'input_type':'password'},
        validators=[validate_password]
    )


    class Meta:
        model=User 
        fields=[
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'password_confirmation'
        ]


    def validate(self, attrs):
        """
        Validation For Checking if the passwords match.
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        if password!= password_confirmation:
            raise serializers.ValidationError(_("Two Password doesn't match "))
        return attrs
    

    def create(self,validated_data):
        """
        Over-riding the create method to create a user
        account 
        """
        try:       
            user=User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            return user 
            
        # ! For handeling expections if any 
        except Exception as e:
            print(f"error --> {e}")
            raise serializers.ValidationError(
                _("Somme Error occoured during registration")
            )
    



#! Serializer for User Login
class UserLoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type':'password'}
    )




# ! Serailizer For Changing Users Password Using Old Password
class UserChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    

    def validate_old_password(self,value):
        """
        Validation for Checking if old password matches or not 
        """
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError(
                _("Current password doesn't match")
                )
        return value
    
    
    def validate(self, attrs):
        """
        Extra Validation of New Password and Old Password
        with New Password
        """
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        new_password_confirmation=attrs.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise serializers.ValidationError(
                _('Two Passwords does not match')
            )
        
        if old_password==new_password:
            raise serializers.ValidationError(
                _('New passwords cannot be similar to current password ')
            )
        
        user=self.context['user']
        user.set_password(new_password)
        user.save()
        return attrs




# ! Serializer For Sending Password Reset Email
class SendResetPasswordEmailSerializer(serializers.Serializer):
      email=serializers.EmailField()

      def validate(self, attrs):
        """
        Validate if User is registered ith given Email 
        if yes call the celery task for sending email
        """
        email=attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with the given email doesn't exist"))

        # ! For Creating a Unique Uid and Token For User 
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)

        link=f'http://127.0.0.1:8000/api/auth/reset-password/{uid}/{token}/'
        subject="Resetting Password"
        email=user.email

        # ! Data For Passing To Celery Task
        data={
            "subject":subject,
            "link":link,
            "to_email":email
        }

        # ! Celery Task For Sending Email
        password_reset_task.delay(data)
        return attrs
       



# ! Serializer For Resetting The Password From The Received Email Link
class PasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )


    def validate(self, attrs):
        """
        Validates the new password and also set the new 
        password for the user 
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        # ! Get the Uid and Token Passed From The View 
        uid=self.context['uid']
        token=self.context['token']

        # ! Decode the User id from the uid
        id=smart_str(urlsafe_base64_decode(uid))

        # ! Validation For Checkng IF Both Password Are The Same
        if password != password_confirmation:
            raise serializers.ValidationError(
                _("Two password field doesn't match")
                )
         
        # ! Check If the User With The Decoded id Exists Or Not
        try:
            user = User.objects.get(id=id)
        # ! IF Not Raises Validation Error
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))
        
        # ! Checks IF The Uid and Token Received Matches With the One 
        # ! Generated For the User Or Not If Not Valdiation Error Is Raised 
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError(_("Token Expired or Invalid"))
        
        # ! Finally Set Password IF no Error is Faced
        user.set_password(password)
        user.save()
        return attrs




# ! Serializer For Changing Email Address 
class SendEmailToChangeEmailSerializer(serializers.Serializer):
    old_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
    )


    def validate_old_password(self,value):
        """
        Validation for Checking if old password matches or not 
        if it matches a email will be sent to a user email with a
        link to change user email address
        """
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError(
                _("Current password doesn't match")
                )
        
        # ! For Creating a Unique Uid and Token For User 
        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)

        link=f'http://127.0.0.1:8000/api/auth/change-email/{uid}/{token}/'
        subject="Change Email Link"
        email=user.email

        # ! Data For Passing To Celery Task
        data={
            "subject":subject,
            "link":link,
            "to_email":email
        }

        # ! Celery Task For Sending Email
        
        change_email_task.delay(data)
        return value





# ! Serializer For Changing Users Email 
class ChangeEmailSerailizer(serializers.Serializer):
    new_email=serializers.EmailField()

    def validate(self, attrs):
        """
        Validate uid and tokens and also validates
        if there is user with the new email provided
        or not if not set it as user new email 
        """
        email=attrs.get('new_email')

        # ! Get the Uid and Token Passed From The View 
        uid=self.context['uid']
        token=self.context['token']

        # ! Decode the User id from the uid
        id=smart_str(urlsafe_base64_decode(uid))

        # ! Checking If the user with given email already exists or not 
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                _("User with this email already exists.")
            )
         
        # ! Check If the User With The Decoded id Exists Or Not
        try:
            user = User.objects.get(id=id)
        # ! IF Not Raises Validation Error
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))
        

        # ! Checks IF The Uid and Token Received Matches With the One 
        # ! Generated For the User Or Not If Not Valdiation Error Is Raised 
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError(_("Token Expired or Invalid"))
        

        # ! Finally Set New Email IF No Error is Faced
        user.email=email
        user.save()
        return attrs


