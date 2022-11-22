from accounts.serializers import CustomUserSerializer
from core.serializers import CommentSerializer, PostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Comment, Post


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({"posts": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_post(request):
    user = request.user
    content = request.data.get("content")

    user_serializer = CustomUserSerializer(user, many=False)

    data = {
        "user": user_serializer.data,
        "content": content
    }
    post_serializer = PostSerializer(data=data, context={"request": request})

    if post_serializer.is_valid():
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_201_CREATED)

    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    is_upvoted = user in post.upvotes.all()
    is_downvoted = user in post.downvotes.all()

    serializer = PostSerializer(post)
    return Response({**serializer.data, "is_upvoted": is_upvoted, "is_downvoted": is_downvoted})


@ api_view(["POST"])
@ permission_classes([IsAuthenticated])
def update_post(request, post_id):
    user = request.user
    content = request.data.get("content")

    user_serializer = CustomUserSerializer(user, many=False)

    data = {
        "user": user_serializer.data,
        "content": content
    }
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    post_serializer = PostSerializer(post, data=data, many=False)

    if post_serializer.is_valid():
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["DELETE"])
@ permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    user = request.user

    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    if post.user == user:
        post.delete()
        return Response({"MSG": "OK"}, status.HTTP_200_OK)
    else:
        return Response({"MSG": "UNAUTHORISED"}, status.HTTP_401_UNAUTHORIZED)


@ api_view(["POST"])
@ permission_classes([IsAuthenticated])
def upvote_post(request, post_id):
    user = request.user

    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    if user in post.upvotes.all():
        post.upvotes.remove(user)
        return Response({"MSG": "Post upvote removed."}, status.HTTP_200_OK)

    else:
        if user in post.downvotes.all():
            post.downvotes.remove(user)
        post.upvotes.add(user)
        return Response({"MSG": "Post upvoted successfully."}, status.HTTP_200_OK)


@ api_view(["POST"])
@ permission_classes([IsAuthenticated])
def downvote_post(request, post_id):
    user = request.user

    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    if user in post.downvotes.all():
        post.downvotes.remove(user)
        return Response({"MSG": "Post downvote removed."}, status.HTTP_200_OK)

    else:
        if user in post.upvotes.all():
            post.upvotes.remove(user)
        post.downvotes.add(user)
        return Response({"MSG": "Post downvoted successfully."}, status.HTTP_200_OK)


@ api_view(["GET"])
@ permission_classes([IsAuthenticated])
def get_post_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(post=post)

    serializer = CommentSerializer(comments, many=True)
    return Response({"comments": serializer.data})


@ api_view(["POST"])
@ permission_classes([IsAuthenticated])
def add_comment(request, post_id):
    user = request.user
    content = request.data.get("content")
    user_serializer = CustomUserSerializer(user, many=False)

    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"MSG": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "user": user_serializer.data,
        "content": content
    }
    comment_serializer = CommentSerializer(
        data=data,
        context={"request": request, "post": post}
    )
    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["POST"])
@ permission_classes([IsAuthenticated])
def update_comment(request, comment_id):
    user = request.user
    content = request.data.get("content")

    user_serializer = CustomUserSerializer(user, many=False)

    data = {
        "user": user_serializer.data,
        "content": content
    }

    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return Response({"MSG": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    comment_serializer = CommentSerializer(comment, data=data, many=False)

    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view(["DELETE"])
@ permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    user = request.user

    try:
        comment = Comment.objects.get(id=comment_id)
    except:
        return Response({"MSG": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

    if user == comment.user:
        comment.delete()
        return Response({"MSG": "OK"}, status.HTTP_200_OK)
    else:
        return Response({"MSG": "UNAUTHORISED"}, status.HTTP_401_UNAUTHORIZED)
