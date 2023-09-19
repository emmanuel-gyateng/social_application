from django.urls import path

from post.views import (CreatePostView, GetAllCommentsForAPostView,
                        GetAllPostView, GetAllUsersPosts, SearchAllPostView,
                        UpdateUserPost, UserAddCommentsToPost,
                        UserLikeOrDislikePost, UserShareOrUnSharePost)

urlpatterns = [
    path("", CreatePostView.as_view(), name="user-create-post"),
    path("search/", SearchAllPostView.as_view(), name="user-search-post"),
    path("all/", GetAllPostView.as_view(), name="user-get-all-posts"),
    path("personal/", GetAllUsersPosts.as_view(), name="user-get-all-personal-posts"),
    path("<int:pk>/", UpdateUserPost.as_view(), name="update-user-post"),
    path("<int:pk>/like", UserLikeOrDislikePost.as_view(), name="like-user-post"),
    path("<int:pk>/share", UserShareOrUnSharePost.as_view(), name="like-user-post"),
    path("<int:pk>/comment", UserAddCommentsToPost.as_view(), name="user-add-comment"),
    path(
        "<int:pk>/comment/all",
        GetAllCommentsForAPostView.as_view(),
        name="user-get-all-comment",
    ),
]
