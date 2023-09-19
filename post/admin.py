from django.contrib import admin

from post.models import Comment, Post, SharedPost

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "content",
        "image",
        "video",
        "get_likes_count",
        "get_shared_by_count",
        "created_at",
    )

    def get_likes_count(self, obj):
        return obj.likes.count()  # Return the count of likes for each post

    get_likes_count.short_description = "Likes Count"  # Column header

    def get_shared_by_count(self, obj):
        return obj.shared_by.count()

    get_shared_by_count.short_description = "Shared_By Count"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "creator",
        "post",
        "comment",
        "parent_comment",
        "created_at",
    )
    list_display_links = (
        "creator",
        "post",
    )


@admin.register(SharedPost)
class SharedPostAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "post",
        "shared_at",
    )
    list_display_links = (
        "user",
        "post",
    )
