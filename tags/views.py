from django.db.models import Count

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Tag
from .serializers import TagSerializer


@api_view(["GET"])
def get_popular_tags(request):
    tags_qs = Tag.objects.annotate(
        posts_count=Count("posts")
    ).order_by("-posts_count")[:10]

    tags_serializer = TagSerializer(tags_qs, many=True)

    return Response({"popular_tags": tags_serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_tags(request):
    user = request.user
    tags_qs = user.tags

    tags_serializer = TagSerializer(tags_qs, many=True)

    return Response({"user_tags": tags_serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_user_tags(request):
    user = request.user
    tags = request.data.get("tags")

    tags_serializer = TagSerializer(
        data=tags,
        many=True
    )
    if tags_serializer.is_valid():
        user.tags.clear()
        for tag_dict in tags_serializer.data:
            tag_name = tag_dict["name"]
            tag_obj = Tag.objects.get(name=tag_name)
            user.tags.add(tag_obj)
        return Response(tags_serializer.data, status=status.HTTP_201_CREATED)
    return Response(tags_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_tags(request):
    tag_query = request.GET.get("query")
    tags_qs = Tag.objects.filter(name__icontains=tag_query)[:1]

    tags_serializer = TagSerializer(tags_qs, many=True)

    return Response({"tags": tags_serializer.data})