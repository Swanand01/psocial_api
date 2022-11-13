from accounts.serializers import CustomUserSerializer
from rest_framework import serializers
from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    content = serializers.CharField(max_length=500)
    upvote_count = serializers.IntegerField(
        source="get_upvote_count", required=False)
    downvote_count = serializers.IntegerField(
        source="get_downvote_count", required=False)
    comment_count = serializers.IntegerField(
        source="get_comment_count", required=False)

    class Meta:
        model = Post
        fields = ("id", "content", "user", "upvote_count",
                  "downvote_count", "comment_count")

    def create(self, validated_data):
        user = self.context.get("request").user
        post = Post.objects.create(user=user, **validated_data)
        return post

    def update(self, instance, validated_data):
        instance.content = validated_data.get("content")
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
