"""Admin User file"""
from django.contrib import admin
from authentications.models import Users

# Register your models here.


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    """Registration of User model class in admin"""

    list_display = (
        "username",
        "email_address",
        "is_active",
        "is_superuser",
    )
    list_display_links = ("email_address",)
    list_editable = ("username",)
