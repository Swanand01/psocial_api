from rest_framework import serializers

from accounts.serializers import CustomUserSerializer
from tags.serializers import TagSerializer
from .models import Comment, Post
from tags.models import Tag


class PostSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    content = serializers.CharField(max_length=500)
    upvote_count = serializers.IntegerField(
        source="get_upvote_count", required=False)
    downvote_count = serializers.IntegerField(
        source="get_downvote_count", required=False)
    comment_count = serializers.IntegerField(
        source="get_comment_count", required=False)
    tags = TagSerializer(many=True, required=True)
    pub_date = serializers.DateTimeField(required=False)

    class Meta:
        model = Post
        fields = ("id", "content", "user", "upvote_count",
                  "downvote_count", "comment_count", "tags", "pub_date")

    def create(self, validated_data):
        user = self.context.get("request").user
        content = validated_data.get("content")
        post = Post.objects.create(user=user, content=content)
        tags = validated_data.get("tags")

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag["name"])
            post.tags.add(tag_obj)

        return post

    def update(self, instance, validated_data):
        content = validated_data.get("content")
        tags = validated_data.get("tags")

        instance.tags.clear()
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(name=tag["name"])
            instance.tags.add(tag_obj)

        instance.content = content
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    content = serializers.CharField(max_length=200)

    class Meta:
        model = Comment
        fields = ("user", "content")

    def create(self, validated_data):
        user = self.context.get("request").user
        post = self.context.get("post")
        content = validated_data.get("content")
        comment = Comment.objects.create(user=user, post=post, content=content)
        return comment

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content")
        instance.save()
        return instance
