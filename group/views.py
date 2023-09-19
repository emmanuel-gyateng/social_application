"""View for Group Application"""
from rest_framework import filters, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentications.models import Users
from exceptions.exceptions import (GroupMemberNotFound, GroupNotFound,
                                   UserNotFound)
from group.models import Group, GroupMember
from group.serializer import (AddUserToGroupSerializer, CreateGroupSerializer,
                              SearchGroupsSerializer)


# Create your views here.
class CreateGroupView(CreateAPIView):
    queryset = Group.objects
    member_queryset = GroupMember.objects
    serializer_class = CreateGroupSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            group = self.queryset.create(**serializer.validated_data)
            self.member_queryset.create(user=request.user, group=group, is_admin=True)
            return Response(
                {"status": "success", "message": "group created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddUsersToGroup(CreateAPIView):
    queryset = GroupMember.objects
    group_queryset = Group.objects
    user_queryset = Users.objects
    serializer_class = AddUserToGroupSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user_id = serializer.validated_data["user_id"]
                is_admin = serializer.validated_data["is_admin"]
                group = self.group_queryset.get(pk=pk)
                user_to_be_added = self.user_queryset.get(pk=user_id)
                user_performing_add = self.queryset.get(user=request.user, group=group)
                if not user_performing_add.is_admin:
                    return Response(
                        {"status": "failure", "message": "user not an admin"}
                    )
                if self.queryset.filter(group=group, user=user_to_be_added).exists():
                    return Response(
                        {
                            "status": "failure",
                            "message": "user already part of the group",
                        },
                        status=status.HTTP_409_CONFLICT,
                    )
                self.queryset.create(
                    group=group, user=user_to_be_added, is_admin=is_admin
                )
                return Response(
                    {
                        "status": "success",
                        "message": "user added to group successfully",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Group.DoesNotExist as exc:
                raise GroupNotFound from exc
            except GroupMember.DoesNotExist as exc:
                raise GroupNotFound from exc
            except Users.DoesNotExist as exc:
                raise UserNotFound from exc
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GroupUpdateOrDeleteView(UpdateAPIView, DestroyAPIView):
    queryset = Group.objects
    member_queryset = GroupMember.objects
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGroupSerializer

    def put(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if self.queryset.filter(pk=pk).exists():
                self.queryset.filter(pk=pk).update(**serializer.validated_data)
                return Response(
                    {"status": "success", "message": "updated successfully"}
                )

    def delete(self, request, pk, *args, **kwargs):
        try:
            if (
                self.member_queryset.filter(group__pk=pk, user=request.user).exists()
                and self.member_queryset.filter(group__pk=pk, user=request.user)
                .first()
                .is_admin
            ):
                self.queryset.get(pk=pk).delete()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            return Response(
                {"status": "failure", "message": "user not admin or not part of group"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Group.DoesNotExist as exc:
            raise GroupNotFound from exc


class UserLeaveGroup(DestroyAPIView):
    queryset = GroupMember.objects
    group_queryset = Group.objects
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def delete(self, request, pk, *args, **kwargs):
        try:
            if not self.queryset.filter(group__pk=pk, user=request.user).exists():
                return Response(
                    {"status": "failure", "message": "user is not part of group"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.queryset.get(group__pk=pk, user=request.user).delete()
            if self.group_queryset.filter(pk=pk).first().members.count() == 0:
                self.group_queryset.get(pk=pk).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except GroupMember.DoesNotExist as exc:
            raise GroupMemberNotFound from exc


class UserJoinGroup(CreateAPIView):
    queryset = GroupMember.objects
    group_queryset = Group.objects

    def get_serializer_class(self):
        return super().get_serializer_class()

    def post(self, request, pk, *args, **kwargs):
        try:
            group = self.group_queryset.get(pk=pk)
            if self.queryset.filter(group__pk=pk, user=request.user).exists():
                return Response(
                    {"status": "failure", "message": "user already part of group"}
                )
            self.queryset.create(user=request.user, group=group)
            return Response(
                {"status": "success", "message": "user joined group successfully"}
            )
        except Group.DoesNotExist as exc:
            raise GroupNotFound from exc


class SearchForGroup(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = SearchGroupsSerializer
    search_fields = ["name"]
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated]
