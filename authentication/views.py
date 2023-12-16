from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND
from .serializers import UserRegistrationSerializer,UserActivationSerializer,UserLoginSerializer,UserChangePasswordSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.utils.translation import gettext_lazy as _ 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User

#! Generates token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[AllowAny]

    def post(self,request) -> Response:
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(_("Registered successfully,Activation link has been sent to your email"),status=HTTP_201_CREATED)

class UserActivationView(APIView):
    serializer_class=UserActivationSerializer

    def post(self,request,**kwargs)-> Response:
        uid=self.kwargs['uid']
        token=self.kwargs['token']
        serializer=self.serializer_class(data=request.data,context={'uid':uid,"token":token})
        serializer.is_valid(raise_exception=True)
        return Response(_("Your account has been successfully activated"),status=HTTP_200_OK)
    
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request)-> Response:
        serailizer=self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)
        email=serailizer.data.get('email')
        password=serailizer.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not  None:
            token=get_tokens_for_user(user)
            return Response({"token":token,"message":"Logged in successfully"},status=HTTP_200_OK)
        else:
            return Response(_("Invalid Credential provided"),status=HTTP_401_UNAUTHORIZED)
            
class UserChangePasswordView(APIView):
    serializer_class=UserChangePasswordSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request) -> Response:
        user=request.user
        serializer=self.serializer_class(data=request.data,context={'user':user})
        serializer.is_valid(raise_exception=True)
        return Response({"message":"Password changed successfully successfully"},status=HTTP_200_OK)

