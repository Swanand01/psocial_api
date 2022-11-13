from django.urls import path

from .views import (
    add_comment,
    get_post_comments,
    update_comment,
    delete_comment,
    get_all_posts,
    create_post,
    get_post,
    update_post,
    delete_post,
    upvote_post,
    downvote_post,
)

urlpatterns = [
    path('get-all-posts/', get_all_posts, name='get_all_posts'),
    path('create-post/', create_post, name='create_post'),
    path('get-post/<str:post_id>/', get_post, name='get_post'),
    path('update-post/<str:post_id>/', update_post, name='update_post'),
    path('delete-post/<str:post_id>/', delete_post, name='delete_post'),
    path('upvote-post/<str:post_id>/', upvote_post, name='upvote_post'),
    path('downvote-post/<str:post_id>/', downvote_post, name='downvote_post'),
    path('get-post-comments/<str:post_id>/',
         get_post_comments, name='get_post_comments'),
    path('add-comment/<str:post_id>/', add_comment, name='add_comment'),
    path('update-comment/<str:comment_id>/',
         update_comment, name='update_comment'),
    path('delete-comment/<str:comment_id>/',
         delete_comment, name='delete_comment')
]
