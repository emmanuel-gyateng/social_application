from django.db import models

from authentications.models import Users


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        Users, on_delete=models.CASCADE, related_name="user_profile"
    )
    full_name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="images/%Y", blank=True, default="images/default.png"
    )
    bio = models.TextField(null=True, blank=True)
    followers = models.ManyToManyField(Users, related_name="followers", blank=True)
    following = models.ManyToManyField(Users, related_name="following", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
