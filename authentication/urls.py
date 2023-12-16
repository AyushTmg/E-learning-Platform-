
from django.urls import path
from .views import UserActivationView,UserRegistrationView,UserLoginView,\
UserChangePasswordView,SendResetPasswordEmailView,PassswordResetView\
,UserProfileView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistrationView.as_view(),name='user-register'),
    path('activate/<str:uid>/<str:token>/',UserActivationView.as_view(),name='user-account-activate'),
    path('login/',UserLoginView.as_view(),name='use-login'),
    path('change-password/',UserChangePasswordView.as_view(),name="user-change-password"),
    path('send-reset-password-email/',SendResetPasswordEmailView.as_view(),name="send-reset-password-email"),
    path('reset-password/<str:uid>/<str:token>/',PassswordResetView.as_view(),name="user-password-reset"),
    path('profile/',UserProfileView.as_view(),name='user-profile')
]