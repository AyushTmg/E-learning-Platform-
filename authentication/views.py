from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND
from .serializers import UserRegistrationSerializer,UserActivationSerializer
from rest_framework.permissions import AllowAny
from django.utils.translation import gettext_lazy as _ 
from .models import User


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
    
