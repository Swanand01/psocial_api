from django.urls import path
from .views import (
    register_user,
    follow_user,
    unfollow_user,
    get_user_profile,
    get_user_posts,
    get_followers,
    get_following
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow-user/<str:to_follow_id>/', follow_user, name='follow_user'),
    path('unfollow-user/<str:following_id>/',
         unfollow_user, name='unfollow_user'),
    path('get-user-profile/<str:user_name>',
         get_user_profile, name='get_user_profile'),
    path('get-followers/<str:user_id>/', get_followers, name='get_followers'),
    path('get-following/<str:user_id>/', get_following, name='get_following'),
    path('get-user-posts/<str:user_id>/', get_user_posts, name='get_user_posts')
]
