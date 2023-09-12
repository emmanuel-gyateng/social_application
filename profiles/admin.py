from django.contrib import admin
from profiles.models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user","full_name","image","get_followers_count","get_following_count","created_at")
    list_display_links =("user",)

    def get_followers_count(self, obj):
        return obj.followers.count()  # Return the count of likes for each post
    get_followers_count.short_description = 'Followers Count'  # Column header
    def get_following_count(self, obj):
        return obj.following.count()  # Return the count of likes for each post
    get_following_count.short_description = 'Following Count'  # Column header

