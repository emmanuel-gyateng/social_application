"""Models for user creation"""
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



# Create your models here.
class AdminUser(BaseUserManager):
    """Registration of the user using the BaseUserManager to create a superuser"""

    def create_user(self, email_address,username=None, password=None):
        """Creation of user"""
        if not email_address:
            raise ValueError("user must have email address")

        user = self.model(
            email_address=email_address,username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password, username=None):
        """Creation of a superuser"""
        user = self.create_user( email_address=email_address,username=username, password=password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    """User creation model"""
    email_address = models.EmailField(
        verbose_name='email', unique=True, max_length=200)
    # full_name = models.CharField(max_length=200, blank=True, unique=False,null=True)
    username = models.CharField(max_length=100, blank=False, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["username"]
    objects = AdminUser()

    class Meta:
        """Pre displayed field"""
        ordering = ("email_address",)

    def __str__(self):
        return f"{self.email_address}"

    def has_perm(self, perm, obj=None):
        """When user registraion has permission, then it is a superuser"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Has permission to access the model, like create a super user"""
        return self.is_superuser