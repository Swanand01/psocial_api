from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField(
        blank=True,
        auto_now_add=True
    )
    upvotes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="post_upvotes"
    )
    downvotes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="post_downvotes"
    )

    def get_upvote_count(self):
        """Returns the number of upvotes on the post"""
        return self.upvotes.count()

    def get_downvote_count(self):
        """Returns the number of downvotes on the post"""
        return self.downvotes.count()

    def get_comment_count(self):
        return self.comments.all().count()

    def get_is_upvoted(self):
        return


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank=True
    )

    def __str__(self):
        return self.content
