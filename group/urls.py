from django.urls import path

from group.views import (AddUsersToGroup, CreateGroupView,
                         GroupUpdateOrDeleteView, SearchForGroup,
                         UserJoinGroup, UserLeaveGroup)

urlpatterns = [
    path("", CreateGroupView.as_view(), name="user-create-group"),
    path("search/", SearchForGroup.as_view(), name="user-search-group"),
    path("<int:pk>/add", AddUsersToGroup.as_view(), name="user-add-others-to-group"),
    path("<int:pk>/", GroupUpdateOrDeleteView.as_view(), name="user-delete-group"),
    path("<int:pk>/leave", UserLeaveGroup.as_view(), name="user-leaves-group"),
    path("<int:pk>/join", UserJoinGroup.as_view(), name="user-joins-group"),
]
