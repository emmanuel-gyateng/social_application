"""User accounts urls"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authentications.views import (ChangePassword, EmailVerification,
                                   RequestResetPasswordEmail,
                                   ResetPasswordLinkVerify, ResetPasswordView,
                                   SearchForUsers, UserDetails, UserLogin,
                                   UserLogOut, UserRegistration)

urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path("", SearchForUsers.as_view(), name="users-search-for-users"),
    path("user/", UserDetails.as_view(), name="details"),
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", UserLogOut.as_view(), name="logout"),
    path("verify-email/", EmailVerification.as_view(), name="email_verify"),
    path("change-password/", ChangePassword.as_view(), name="change_password"),
    path("reset-password/", RequestResetPasswordEmail.as_view(), name="reset-password"),
    path(
        "reset-password/confirm/",
        ResetPasswordLinkVerify.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "reset-password/done/", ResetPasswordView.as_view(), name="reset-password-done"
    ),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
