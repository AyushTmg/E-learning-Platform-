from .serializers import (
    UserLoginSerializer,
    PasswordResetSerializer,
    UserRegistrationSerializer,
    UserChangePasswordSerializer,
    SendResetPasswordEmailSerializer,
)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
)


from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _ 




#! Generates token manually
def get_tokens_for_user(user):
    """
    Custom function to generate and return access and
    refresh tokens for a user after successful login
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }




# ! View For User Registration 
class UserRegistrationView(APIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[AllowAny]


    def post(self,request) -> Response:
        """
        Register a new user in the system.
        """
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            _("Your account has been successfully registered"),
            status=HTTP_201_CREATED
        )




# ! View For User Login 
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request)-> Response:
        """
        Method to Logs in an as existing user and generates tokens
        for them to access our API if exists else return Error.
        """
        serailizer=self.serializer_class(data=request.data)
        serailizer.is_valid(raise_exception=True)

        # ! Gets the validated data from the serializer 
        email=serailizer.data.get('email')
        password=serailizer.validated_data.get('password')

        # ! Checks if the user exists with the given credentials or not
        user=authenticate(email=email,password=password)

        # ! If a User exists  then generate Token for that user
        if user is not  None:
            token=get_tokens_for_user(user)
            return Response(
                {"token":token,"message":"Logged in successfully"},
                status=HTTP_200_OK
            )
        
        # ! If User Doesn't exists or Invalid Credintials 
        return Response(
            _("Invalid Credential provided"),
            status=HTTP_401_UNAUTHORIZED
        )

  


# ! View For Changing Password 
class UserChangePasswordView(APIView):
    serializer_class=UserChangePasswordSerializer
    permission_classes=[IsAuthenticated]


    def post(self,request) -> Response:
        """
        Changes Logged in Users Password with the help
        of current password
        """
        user=request.user
        serializer=self.serializer_class(
            data=request.data,
            context={'user':user}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message":"Password changed successfully successfully"},
            status=HTTP_200_OK
        )




# ! View For Sending Email For Password Reset
class SendResetPasswordEmailView(APIView):
    serializer_class=SendResetPasswordEmailSerializer
    permission_classes=[AllowAny]

    def post(self,request) -> Response:
        """
        Sends an email to the registered user for 
        reseting his/her password.
        """
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            _("Reset Password Email has been sent to the email"),
            status=HTTP_200_OK
        )
    



# ! View For Resetting User Password
class PassswordResetView(APIView):
    serializer_class=PasswordResetSerializer

    def post(self,request,**kwargs) -> Response:
        """
        Validates and resets the password of a user by 
        passing the uid and token from the URL Parameter
        """
        uid=self.kwargs['uid']
        token=self.kwargs['token']

        serializer=self.serializer_class(
            data=request.data,
            context={'uid':uid,'token':token}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            _("Password successfully changed"),
            status=HTTP_200_OK
        )





