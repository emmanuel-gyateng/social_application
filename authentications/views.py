"""VIews for Authentications application"""
from django.contrib.auth.tokens import default_token_generator
from rest_framework import filters, status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from authentications.models import Users
from authentications.serializer import (ChangePasswordSerializer,
                                        ListUsersSerializer,
                                        MyTokenObtainPairSerializer,
                                        RegistrationSerializer,
                                        RequestPasswordResetEmail,
                                        ResetPasswordSerializer,
                                        UserDetailSerializer,
                                        UserLogOutSerializer)
from exceptions.exceptions import InvalidLink, UserNotFound
from profiles.models import Profile
from utils.email_service import (send_email_verification_mail,
                                 send_reset_password_email)


class UserRegistration(GenericAPIView):
    """User resgistration view class"""

    profile_queryset = Profile.objects
    queryset = Users.objects
    serializer_class = RegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        """Post request for user registration"""
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid():
            self.queryset.create_user(
                username=serializers.validated_data["username"],
                email_address=serializers.validated_data["email_address"],
                password=serializers.validated_data["password"],
            )
            user = self.queryset.get(
                email_address=serializers.validated_data["email_address"]
            )
            email = serializers.validated_data["email_address"]
            full_name = serializers.validated_data["full_name"]
            username = serializers.validated_data["username"]
            confirmation_token = default_token_generator.make_token(user)
            self.profile_queryset.create(user=user, full_name=full_name)
            send_email_verification_mail.delay(
                username=username, email=email, token=confirmation_token
            )
            return Response(
                {
                    "status": "sucess",
                    "detail": "user created successfully",
                    "data": {
                        "email_address": email,
                        "username": serializers.validated_data["username"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "failure", "detail": serializers.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailVerification(APIView):
    """Email Verification"""

    queryset = Users.objects

    def get(self, request):
        """Getting the token and email from user verification link"""
        try:
            user = self.queryset.get(email_address=request.GET["iam"])
            token = request.GET["def"]
            if default_token_generator.check_token(user, token):
                if user.is_active:
                    return Response(
                        {
                            "status": "failure",
                            "detail": "email already verified",
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
                else:
                    user.is_active = True
                    user.save()
                    return Response(
                        {
                            "status": "sucess",
                            "detail": "email verified successful",
                            "data": {"is_active": user.is_active},
                        },
                        status=status.HTTP_200_OK,
                    )
            else:
                raise InvalidLink
        except Users.DoesNotExist as exc:
            raise UserNotFound from exc


class UserLogin(TokenObtainPairView):
    """Overiding the TokenObtainPiarView of simple jwt to login user"""

    serializer_class = MyTokenObtainPairSerializer


class ChangePassword(GenericAPIView):
    """User change password view endpoint where both users can change their password"""

    queryset = Users.objects
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        """Making a PUT request to change passowrd by both user and superuser"""
        user = self.queryset.get(email_address=request.user)
        serializer = self.serializer_class(data=request.data)
        try:
            if serializer.is_valid():
                if not user.check_password(serializer.data.get("old_password")):
                    return Response(
                        {
                            "status": "failure",
                            "detail": "wrong old password",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(serializer.data.get("new_password"))
                user.is_changed_password = True
                user.save()
                return Response(
                    {
                        "status": "success",
                        "detail": "Password changed successfully",
                        "data": {
                            "username": user.username,
                            "email_address": user.email_address,
                            "is_admin": user.is_staff,
                            "is_superuser": user.is_superuser,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except KeyError:
            return Response(
                {"status": "failure", "detail": "change password failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLogOut(GenericAPIView):
    """Logout API view to blacklist refresh token"""

    serializer_class = UserLogOutSerializer
    queryset = Users.objects
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Reseting refresh token to blacklist it from getting new token"""
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"status": "success", "detail": "logout successful"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except KeyError:
            return Response(
                {"status": "failure", "detail": "Logout Unsuccessful"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RequestResetPasswordEmail(GenericAPIView):
    """VIew for user to request password change email"""

    queryset = Users.objects
    serializer_class = RequestPasswordResetEmail
    permission_classes = []

    def post(self, request):
        """Post request to this view"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email_address"]
                user = self.queryset.get(email_address=email)
                password_reset_token = default_token_generator.make_token(user)
                send_reset_password_email.delay(
                    username=user.username, email=email, token=password_reset_token
                )
                return Response({"status": "sucess", "detail": "reset email sent"})
            except Users.DoesNotExist as exc:
                raise UserNotFound from exc
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordLinkVerify(GenericAPIView):
    """Verification of the link sent to user when they try to access the link"""

    queryset = Users.objects
    serializer_class = RequestPasswordResetEmail
    permission_classes = []

    def get(self, request):
        """A get request with query parameters"""
        try:
            user = self.queryset.get(email_address=request.GET["iam"])
            token = request.GET["def"]
            if default_token_generator.check_token(user, token):
                return Response(
                    {
                        "status": "sucess",
                        "detail": "link verified successful",
                        "data": {"email_address": user.email_address},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise InvalidLink
        except Users.DoesNotExist as exc:
            raise UserNotFound from exc


class ResetPasswordView(GenericAPIView):
    """The actual reset password view where the user enters the password"""

    queryset = Users.objects
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request):
        """Post request with link token, password and email address"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                email = serializer.validated_data["email_address"]
                token = serializer.validated_data["token"]
                password = serializer.validated_data["password"]
                user = self.queryset.get(email_address=email)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return Response(
                        {"status": "success", "detail": "Password reset successful"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"status": "failure", "detail": "token invalid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Users.DoesNotExist as exc:
                raise UserNotFound from exc
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetails(GenericAPIView):
    """View for getting user details with tokens"""

    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Get function request"""
        user = request.user
        serializer = self.serializer_class(user)
        return Response(
            {
                "status": "success",
                "detail": "User details found",
                "data": {
                    "id": serializer.data["id"],
                    "username": serializer.data["username"],
                    "email_address": serializer.data["email_address"],
                    "is_admin": serializer.data["is_admin"],
                    "is_superuser": serializer.data["is_superuser"],
                },
            }
        )


class SearchForUsers(ListAPIView):
    queryset = Users.objects.all()
    serializer_class = ListUsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ["username", "email_address"]
    permission_classes = [IsAuthenticated]
