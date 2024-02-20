from .views import (
    UserRegistrationView,
    UserLoginView,
    UserChangePasswordView,
    SendResetPasswordEmailView,
    PassswordResetView,
)


from rest_framework_simplejwt.views import ( TokenRefreshView)
from django.urls import path



urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegistrationView.as_view(),name='user-register'),
    path('login/',UserLoginView.as_view(),name='user-login'),
    path('change-password/',UserChangePasswordView.as_view(),name="user-change-password"),
    path('send-reset-password-email/',SendResetPasswordEmailView.as_view(),name="send-reset-password-email"),
    path('reset-password/<str:uid>/<str:token>/',PassswordResetView.as_view(),name="user-password-reset"),
]