from django.urls import path

from profiles.views import (GetUserProfile, GetUserProfileById,
                            GetUserProfileByUserId, UpdateProfileOfUser,
                            UserFollowOtherUsersView)

urlpatterns = [
    path("", GetUserProfile.as_view(), name="user-profile"),
    path("basic/", UpdateProfileOfUser.as_view(), name="user-update-profile"),
    path("follow/", UserFollowOtherUsersView.as_view(), name="user-follow-or-unfollow"),
    path("<int:pk>/", GetUserProfileById.as_view(), name="user-get-other-profile"),
    path(
        "user/<int:pk>/",
        GetUserProfileByUserId.as_view(),
        name="user-get-other-profile-by-user-id",
    ),
]
