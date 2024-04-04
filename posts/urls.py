from django.urls import path
from . import views

urlpatterns = [
    # * http://127.0.0.1/posts/ *#
    # Post URLs #
    path(
        "new/", views.CreatePostAPI.as_view(), name="new-post"
    ),  # Create a new post. (POST)
    path(
        "all/", views.ListAllPostsAPI.as_view(), name="all-posts"
    ),  # List all posts. (GET)
    path(
        "detail-post/<int:pk>/", views.DetailPostAPI.as_view(), name="detail-post"
    ),  # Detailed post by pk. (GET, PUT, PATCH, DELETE)
    path(
        "detail-post/<str:post_slug>/",
        views.SlugPostAPI.as_view(),
        name="detail-post-by-slug",
    ),  # Detailed post by slug. (GET)
    path(
        "featured/", views.GetFeaturedPosts.as_view(), name="featured-posts"
    ),  # List of all Featured Posts. (GET)
    path(
        "top/", views.GetTopPosts.as_view(), name="top-posts"
    ),  # List of all latest Top Posts. (GET)
    path(
        "popular/", views.GetPopularPosts.as_view(), name="popular-posts"
    ),  # List of all latest Top Posts. (GET)
    path(
        "trending/", views.GetTrendingPosts.as_view(), name="trending-posts"
    ),  # List of all latest Top Posts. (GET)
    path(
        "premium/", views.PremiumPostsList.as_view(), name="premium-post"
    ),  # Lists of all Premium posts for all Premium Users.
    # Comment URLs #
    path(
        "comment/all/", views.ListComments.as_view(), name="list-all-comments"
    ),  # List all comments. (GET)
    path(
        "comment/add/", views.CreateComment.as_view(), name="add-comment"
    ),  # Create a new comment. (POST)
    path(
        "comment/<int:pk>/", views.DetailComment.as_view(), name="detail-comment"
    ),  # Create a new comment. (POST)
    path(
        "comment/post/<int:post>", views.GetPostComments.as_view(), name="post-comments"
    ),
    path(
        "comment/post/<str:slug>",
        views.GetPostCommentsbySlug.as_view(),
        name="post-comments",
    ),
    # Like URLs #
    path(
        "like/all/", views.ListAllLikes.as_view(), name="list-all-likes"
    ),  # List all likes. (GET)
    path(
        "like/add/", views.CreateLike.as_view(), name="add-like"
    ),  # Add a new like to a post or comment. (POST)
    path(
        "like/delete/post/<int:post>/<int:user>/",
        views.DestroyPostLike.as_view(),
        name="destroy-like-post",
    ),  # Destroy / Remove a like on Post. (DELETE)
    path(
        "like/delete/comment/<int:comment>/<int:user>/",
        views.DestroyCommentLike.as_view(),
        name="destroy-like-comment",
    ),  # Destroy / Remove a like on Comment. (DELETE)
    path(
        "like/get/post/<int:user_id>/<int:post_id>/",
        views.GetLikebyUserPost.as_view(),
        name="get-user-like-by-post",
    ),
    # PostHistory URLs #
    path(
        "history/", views.ListAllPostsHistory.as_view(), name="list-all-history"
    ),  # List all Editing Logs. (GET)
    path(
        "history/<int:post_id>",
        views.ListSinglePostHistory.as_view(),
        name="list-all-history-of-post",
    ),  # List all Editing History of a Single Post. (GET)
    # Contact Form #
    path("contact/", views.SendEmailView.as_view(), name="contact-form"),
    # Notifications URLs #
    path(
        "notifications/", views.NotificationsList.as_view(), name="all-notifications"
    ),  # Get list of all the notifications in the database. (GET)
    path(
        "notifications/<int:user_id>",
        views.UserNotificationList.as_view(),
        name="all-notifications-by-userid",
    ),  # Get list of all the specific user notification in the database. (GET)
    path(
        "notification/update/<int:pk>",
        views.DetailedNotification.as_view(),
        name="update-notification",
    ),  # Update a notification. (PUT, PATCH)
]
