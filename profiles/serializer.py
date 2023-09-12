from rest_framework import serializers

from profiles.models import Profile


class UpdateUserFullNameAndImageSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)


class UserProfileSerializer(serializers.ModelSerializer):
    """serializer for getting user profile"""

    following_count = serializers.ReadOnlyField(source="following.count")
    followers_count = serializers.ReadOnlyField(source="followers.count")

    class Meta:
        """The base setting of this class"""

        model = Profile
        exclude = (
            "updated_at",
            "created_at",
        )


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("image", "bio", "full_name")


class UserFollowOrUnfollowOtherUsersSerializer(serializers.Serializer):
    folow = serializers.BooleanField()
    user_id = serializers.IntegerField()
