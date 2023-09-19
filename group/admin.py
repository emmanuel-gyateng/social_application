from django.contrib import admin

from group.models import Group, GroupMember


# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_members_count", "created_at")
    list_display_links = ("name",)

    def get_members_count(self, obj):
        return obj.members.count()

    get_members_count.short_description = "Members Count"


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "group", "joined_at", "is_admin")
    list_display_links = ("user",)
