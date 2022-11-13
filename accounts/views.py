from accounts.models import FollowerFollowing
from core.models import Post
from core.serializers import PostSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegistrationSerializer, FollowerSerializer, FollowingSerializer


@api_view(["POST"])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, to_follow_id):
    follower = request.user

    try:
        to_follow = get_user_model().objects.get(id=to_follow_id)
    except get_user_model().DoesNotExist:
        return Response({"MSG": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if follower == to_follow:
        return Response({"MSG": "Cannot follow self."}, status=status.HTTP_400_BAD_REQUEST)

    if not FollowerFollowing.objects.filter(follower=follower, following=to_follow).exists():
        follower_following = FollowerFollowing(
            follower=follower,
            following=to_follow
        )
        follower_following.save()
        return Response({"MSG": "Follower added successfully"}, status=status.HTTP_201_CREATED)

    return Response({"MSG": "FollowerFollowing relation already exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, following_id):
    follower = request.user

    try:
        to_follow = get_user_model().objects.get(id=following_id)
    except get_user_model().DoesNotExist:
        return Response({"MSG": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if follower == to_follow:
        return Response({"MSG": "Cannot unfollow self."}, status=status.HTTP_400_BAD_REQUEST)

    if FollowerFollowing.objects.filter(follower=follower, following=to_follow).exists():
        follower_following = FollowerFollowing.objects.get(
            follower=follower,
            following=to_follow
        )
        follower_following.delete()
        return Response({"MSG": "User unfollowed successfully"}, status=status.HTTP_201_CREATED)

    return Response({"MSG": "FollowerFollowing relation does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_followers(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return Response({"MSG": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    followers = FollowerFollowing.objects.filter(
        following=user).select_related("follower")
    serializer = FollowerSerializer(followers, many=True)
    return Response({"followers": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_following(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return Response({"MSG": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    following = FollowerFollowing.objects.filter(
        follower=user).select_related("following")
    serializer = FollowingSerializer(following, many=True)
    return Response({"followings": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_posts(request, user_id):
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return Response({"MSG": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    posts = Post.objects.filter(user=user)
    serializer = PostSerializer(posts, many=True)
    return Response({"posts": serializer.data}, status=status.HTTP_200_OK)
