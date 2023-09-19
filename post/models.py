from django.db import models

from authentications.models import Users

# Create your models here.


class Post(models.Model):
    POST_TYPES = (
        ("text", "Text"),
        ("image", "Image"),
        ("video", "Video"),
    )
    creator = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="content_creator",
        blank=True,
        null=True,
    )
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/%Y", blank=True, null=True)
    video = models.FileField(upload_to="videos/%Y", blank=True, null=True)
    likes = models.ManyToManyField(Users, related_name="liked_posts", blank=True)
    shared_by = models.ManyToManyField(
        Users, through="SharedPost", related_name="shared_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    creator = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="comment_creator"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replied"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class SharedPost(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
