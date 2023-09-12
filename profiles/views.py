"""View.py file for user profiles urls"""
from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentications.models import Users
from exceptions.exceptions import ProfileNotFound, UserNotFound
from profiles.models import Profile
from profiles.serializer import (UpdateUserFullNameAndImageSerializer,
                                 UpdateUserProfileSerializer,
                                 UserFollowOrUnfollowOtherUsersSerializer,
                                 UserProfileSerializer)


# Create your views here.
class GetUserProfile(RetrieveAPIView):
    queryset = Profile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class GetUserProfileById(RetrieveAPIView):
    queryset = Profile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(pk=self.kwargs["pk"]).first()


class GetUserProfileByUserId(RetrieveAPIView):
    queryset = Profile.objects
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(user__pk=self.kwargs["pk"]).first()


class UpdateUserFullNameAndImageView(GenericAPIView):
    queryset = Profile.objects
    serializer_class = UpdateUserFullNameAndImageSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user_profile = self.queryset.get(user=request.user)
            serializer = self.serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                full_name = request.data["full_name"]
                if len(request.FILES) > 0:
                    image = request.FILES["image"]
                    user_profile.image = image
                if len(full_name) > 0:
                    user_profile.user.full_name = full_name
                    user_profile.user.save()
                user_profile.save()

                return Response(
                    {
                        "status": "success",
                        "data": {
                            "id": user_profile.id,
                            "full_name": user_profile.user.full_name,
                            "image": user_profile.image.url,
                        },
                    }
                )

            return Response(
                {"status": "failure", "detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Profile.DoesNotExist as asc:
            raise ProfileNotFound from asc


class UpdateProfileOfUser(UpdateAPIView):
    serializer_class = UpdateUserProfileSerializer
    queryset = Profile.objects
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(user=self.request.user).first()


class UserFollowOtherUsersView(CreateAPIView):
    queryset = Profile.objects
    user_queryset = Users.objects
    serializer_class = UserFollowOrUnfollowOtherUsersSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_id = serializer.validated_data["user_id"]
                follow = serializer.validated_data["folow"]
                user_to_follow = self.user_queryset.get(pk=user_id)
                profile_of_follower = self.queryset.get(user=user_to_follow)
                current_user_porfile = self.queryset.get(user=request.user)
                print(follow)
                if (
                    follow
                    and not profile_of_follower.followers.contains(user_to_follow)
                    and user_id != request.user.pk
                ):
                    profile_of_follower.followers.add(request.user)
                    current_user_porfile.following.add(user_to_follow)
                if (
                    not follow
                    and profile_of_follower.followers.contains(request.user)
                    and user_id != request.user.pk
                ):
                    profile_of_follower.followers.remove(request.user)
                    current_user_porfile.following.remove(user_to_follow)
                profile_of_follower.save()
                current_user_porfile.save()
                return Response(
                    {"status": "success", "message": "follow action successful"}
                )
            except Profile.DoesNotExist as asc:
                raise ProfileNotFound from asc
            except Users.DoesNotExist as asc:
                raise UserNotFound from asc
        return Response(
            {"status": "failure", "detail": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
