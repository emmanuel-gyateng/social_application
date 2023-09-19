"""View for post"""
from rest_framework import filters, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from exceptions.exceptions import CommentNotFound, PostNotFound
from post.models import Comment, Post, SharedPost
from post.serializer import (CreatePostSerializer, GetAllPostSerializer,
                             UpdateAPostSerilizer,
                             UserAddCommentToAPostSerializer,
                             UserGetAllCommentsForAPost,
                             UserLikePostSerializer, UserSharePostSerializer)

# Create your views here.


class CreatePostView(CreateAPIView):
    queryset = Post.objects
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.queryset.create(creator=request.user, **serializer.validated_data)
            return Response(
                {
                    "status": "success",
                    "message": "post created success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetAllPostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = GetAllPostSerializer
    permission_classes = [IsAuthenticated]


class GetAllUsersPosts(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = GetAllPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.filter(creator=self.request.user).all()


class UpdateUserPost(UpdateAPIView, DestroyAPIView):
    queryset = Post.objects
    serializer_class = UpdateAPostSerilizer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if self.queryset.filter(pk=pk).exists():
                self.queryset.filter(pk=pk).update(**serializer.validated_data)
                return Response(
                    {"status": "success", "message": "updated successfully"}
                )
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, *args, **kwargs):
        if self.queryset.filter(creator=request.user, pk=pk).exists():
            self.queryset.get(pk=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                "status": "failure",
                "message": "delete not successful",
            }
        )


class UserLikeOrDislikePost(GenericAPIView):
    queryset = Post.objects
    serializer_class = UserLikePostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                post = self.queryset.get(pk=pk)
                if serializer.validated_data["is_liked"] and not post.likes.contains(
                    request.user
                ):
                    post.likes.add(request.user)
                    post.save()
                if not serializer.validated_data["is_liked"] and post.likes.contains(
                    request.user
                ):
                    post.likes.remove(request.user)
                    post.save()
                return Response({"status": "success", "message": "action success"})

            except Post.DoesNotExist as exc:
                raise PostNotFound from exc
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserShareOrUnSharePost(CreateAPIView):
    shared_queryset = SharedPost.objects
    queryset = Post.objects
    permission_classes = [IsAuthenticated]
    serializer_class = UserSharePostSerializer

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                post = self.queryset.get(pk=pk)
                if (
                    not self.shared_queryset.filter(
                        user=request.user, post=post
                    ).exists()
                    and serializer.validated_data["is_shared"]
                ):
                    self.shared_queryset.create(user=request.user, post=post)
                if (
                    self.shared_queryset.filter(user=request.user, post=post).exists()
                    and not serializer.validated_data["is_shared"]
                ):
                    self.shared_queryset.filter(
                        user=request.user, post=post
                    ).first().delete()
                return Response({"status": "success", "message": "post action success"})
            except Post.DoesNotExist as exc:
                raise PostNotFound from exc
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserAddCommentsToPost(CreateAPIView, DestroyAPIView):
    queryset = Comment.objects
    post_queryset = Post.objects
    serializer_class = UserAddCommentToAPostSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                post = self.post_queryset.get(pk=pk)
                self.queryset.create(
                    creator=request.user, post=post, **serializer.validated_data
                )
                return Response(
                    {
                        "status": "success",
                        "message": "comment saved success",
                    }
                )
            except Post.DoesNotExist as exc:
                raise PostNotFound from exc
        return Response(
            {"status": "failure", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk, *args, **kwargs):
        try:
            self.queryset.get(creator=request.user, pk=pk).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist as exc:
            raise CommentNotFound from exc


class GetAllCommentsForAPostView(ListAPIView):
    queryset = Comment.objects
    serializer_class = UserGetAllCommentsForAPost
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(post__pk=self.kwargs["pk"]).all()


class SearchAllPostView(ListAPIView):
    serializer_class = GetAllPostSerializer
    search_fields = ["creator__username", "content", "image", "video"]
    filter_backends = (filters.SearchFilter,)
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
