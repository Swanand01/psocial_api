from accounts.models import FollowerFollowing
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            'user_name',
            'password',
            'password2',
            'email'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            user_name=validated_data['user_name'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "user_name")


class FollowerSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(read_only=True)
    date_time = serializers.DateTimeField()

    class Meta:
        model = FollowerFollowing
        fields = ("follower", "date_time")


class FollowingSerializer(serializers.ModelSerializer):
    following = CustomUserSerializer(read_only=True)

    class Meta:
        model = FollowerFollowing
        fields = ("following", "date_time")
