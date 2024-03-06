from django.urls import path
from . import views

urlpatterns = [

    # * http://127.0.0.1/posts/ *#

    # Post URLs #
    path('new/',views.CreatePostAPI.as_view(), name = 'new-post'), # Create a new post. (POST) 
    path('all/',views.ListAllPostsAPI.as_view(), name = 'all-posts'), # List all posts. (GET)
    path('detail-post/<int:pk>/', views.DetailPostAPI.as_view(), name = 'detail-post'), # Detailed post by pk. (GET, PUT, PATCH, DELETE)
    path('detail-post/<str:post_slug>/', views.SlugPostAPI.as_view(), name = 'detail-post-by-slug'), # Detailed post by slug. (GET)
    path('featured/', views.GetFeaturedPosts.as_view(), name = 'featured-posts'), # List of all Featured Posts. (GET)
    path('top/', views.GetTopPosts.as_view(), name = 'top-posts'), # List of all latest Top Posts. (GET)
    path('popular/', views.GetPopularPosts.as_view(), name = 'popular-posts'), # List of all latest Top Posts. (GET)
    path('trending/', views.GetTrendingPosts.as_view(), name = 'trending-posts'), # List of all latest Top Posts. (GET)


    # Comment URLs #
    path('comment/all/', views.ListComments.as_view(), name = 'list-all-comments'), # List all comments. (GET)
    path('comment/add/', views.CreateComment.as_view(), name = 'add-comment'), # Create a new comment. (POST)
    path('comment/<int:pk>/', views.DetailComment.as_view(), name = 'detail-comment'), # Create a new comment. (POST)
    path('comment/post/<int:post>', views.GetPostComments.as_view(), name = 'post-comments'),

    # Like URLs #
    path('like/all/', views.ListAllLikes.as_view(), name = 'list-all-likes'), # List all likes. (GET)
    path('like/add/', views.CreateLike.as_view(), name = 'add-like'), # Add a new like to a post or comment. (POST)
    path('like/delete/post/<int:post>/<int:user>/', views.DestroyPostLike.as_view(), name = 'destroy-like-post'), # Destroy / Remove a like on Post. (DELETE)
    path('like/delete/comment/<int:comment>/<int:user>/', views.DestroyCommentLike.as_view(), name = 'destroy-like-comment'), # Destroy / Remove a like on Comment. (DELETE)


    # PostHistory URLs #
    path('history/', views.ListAllPostsHistory.as_view(), name = 'list-all-history'), # List all Editing Logs. (GET) 
    path('history/<int:post_id>', views.ListSinglePostHistory.as_view(), name = 'list-all-history-of-post'), # List all Editing History of a Single Post. (GET)

    # Contact Form #
    path('contact/', views.SendEmailView.as_view(), name = 'contact-form')
]

# * NEW TODOS * #

"""

TODO: 1. Implement Views on Blog Posts. (Done)
TODO: 2. Add TimeDate Field in Post Model. (Done)
TODO: 3. Create some logic / algo for Popular and Trending Posts.(Featured and Top Post (Done), Popular (Done), Trending(Done))
TODO: 4. Implement Content Scheduling. (Done)
TODO: 5. Implement version history. (Done)
TODO: 6. WYSIWYG Editor. (can be implemented in Admin Panel.)

TODO: 7. Permissions (All Done)
TODO: 8. Create Collection of APIs in Postman. (Majorly Done, will have to add according to requirements)
TODO: 9. Write Tests for APIs. (Do later, this task not given yet)
TODO 10. Implement Newsletter. (Done)
TODO 11. Found a bug, with data/time field. Cannot add date/time manually due to auto_add_on. (Start from here)
        - Have to fix this bug first, else scheduling won't be working.
TODO 12. Make new APIs / Views for Premium Users. (Check if I can make changes at basic views.)

"""