from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User,Profile
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes
from .utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])
    password_confirmation=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])

    class Meta:
        model=User 
        fields=['first_name','last_name','birth_date','email','password','password_confirmation']

    def validate(self, attrs):
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')
        if password!= password_confirmation:
            raise serializers.ValidationError(_("Two Password doesn't match "))
        return attrs
    
    def create(self,validated_data):
        try:
            user=User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                birth_date=validated_data['birth_date'],
                email=validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.save()
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link=f'http://127.0.0.1:8000/api/user/activate/{uid}/{token}/'
            body=f"Click on this link for activating users account {link}"
            subject="Account activation"
            email=user.email
            data={
                "subject":subject,
                "body":body,
                "to_email":email
            }
            Util.send_email(data)
            return user 
        except Exception as e:
            print(f"error --> {e}")
            raise serializers.ValidationError(_("Somme Error occoured during registration"))
    
class UserActivationSerializer(serializers.Serializer):
    def validate(self, attrs):
        try:
            uid=self.context['uid']
            token=self.context['token']
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError(_("Tokens doesn't match or is exprired"))
            user.is_active=True
            user.save()
            return attrs
        except Exception as e:
            print(f"error --> {e}")
            raise serializers.ValidationError(_("Somme Error occoured during activation"))

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']

class UserChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])
    new_password=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])
    new_password_confirmation=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])
    

    def validate_old_password(self,value):
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError(_("Current password doesn't match"))
        return value
    
    def validate(self, attrs):
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        new_password_confirmation=attrs.get('new_password_confirmation')
        if new_password != new_password_confirmation:
            raise serializers.ValidationError(_('Two Passwords does not match'))
        if old_password==new_password:
            raise serializers.ValidationError(_('New passwords cannot be similar to current password '))
        user=self.context['user']
        user.set_password(new_password)
        user.save()
        return attrs

class SendResetPasswordEmailSerializer(serializers.Serializer):
      email=serializers.EmailField()

      def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link=f'http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}/'
            subject="Resetting Password"
            body=f"Click on the link for resetting password {link}"
            email=user.email
            data={
                "subject":subject,
                "body":body,
                "to_email":email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError(_("User with the given email doesn't exist"))
        
        
class PasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])
    password_confirmation=serializers.CharField(style={'input_type':'password'},write_only=True,validators=[validate_password])

    def validate(self, attrs):
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')
        uid=self.context['uid']
        token=self.context['token']
        id=smart_str(urlsafe_base64_decode(uid))

        if password != password_confirmation:
            raise serializers.ValidationError(_("Two password field doesn't match"))
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User not found"))
        
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError(_("Token Expired or Invalid"))
        
        user.set_password(password)
        user.save()
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    class Meta:
        model=Profile 
        fields=['user','username','bio','phone','location']
    
 
    

    
    