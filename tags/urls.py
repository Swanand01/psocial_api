from django.urls import path

from .views import get_popular_tags, get_user_tags, update_user_tags, search_tags

urlpatterns = [
    path('get-popular-tags/', get_popular_tags, name='get_popular_tags'),
    path('get-user-tags/', get_user_tags, name="get_user_tags"),
    path('update-user-tags/', update_user_tags, name="update_user_tags"),
    path('search-tags/', search_tags, name="search_tags")
]
