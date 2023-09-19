from rest_framework import serializers

from post.models import Comment, Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = (
            "creator",
            "likes",
            "shared_by",
            "created_at",
        )


class GetAllPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.ReadOnlyField(source="likes.count")
    shared_count = serializers.ReadOnlyField(source="shared_by.count")
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    class Meta:
        model = Post
        fields = "__all__"


class UpdateAPostSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = (
            "creator",
            "likes",
            "shared_by",
            "created_at",
        )


class UserLikePostSerializer(serializers.Serializer):
    is_liked = serializers.BooleanField()


class UserSharePostSerializer(serializers.Serializer):
    is_shared = serializers.BooleanField()


class UserAddCommentToAPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment", "parent_comment")
        extra_kwargs = {"parent_comment": {"required": False}}


class UserGetAllCommentsForAPost(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
