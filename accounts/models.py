from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth import get_user_model
from django.urls import reverse
from tags.models import Tag


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, user_name, email, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not user_name:
            raise ValueError('Users must have an username')

        if not email:
            raise ValueError('Users must have an email')

        # if not password:
        #     raise ValueError('Users must have an password')

        user = self.model(
            user_name=user_name,
            email=email
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, user_name, email, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        if not password:
            raise ValueError('Users must have an password')

        user = self.create_user(
            user_name=user_name,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """The Custom User model"""
    user_name = models.CharField(max_length=25, unique=True)
    email = models.EmailField(blank=True, unique=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag)
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def get_follower_count(self):
        """Returns the user's followers"""
        return self.follower.count()

    @property
    def get_following_count(self):
        """Returns the user's followings"""
        return self.following.count()

    def __str__(self):
        return self.user_name + " " + str(self.id)

    # @property
    # def get_profile_image(self):
    #     try:
    #         return self.profile_image.get_image_url
    #     except:
    #         return ""

    # def get_profile_url(self):
    #     """Returns the profile page url for the user."""
    #     return reverse("profile", kwargs={
    #         "user_name": self.user_name
    #     })


class FollowerFollowing(models.Model):
    follower = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='follower')
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"
