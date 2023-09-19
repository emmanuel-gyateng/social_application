"""Serializer class for group request and responses"""
from rest_framework import serializers

from authentications.models import Users
from group.models import Group, GroupMember


class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class AddUserToGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = GroupMember
        fields = ("is_admin", "user_id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


class SearchGroupsSerializer(serializers.ModelSerializer):
    members_count = serializers.ReadOnlyField(source="members.count")

    class Meta:
        model = Group
        fields = "__all__"
