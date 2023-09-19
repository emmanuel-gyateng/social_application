from django.db import models

from authentications.models import Users


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=100, unique=False)
    members = models.ManyToManyField(Users, through="GroupMember")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class GroupMember(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
