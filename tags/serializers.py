from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)

    class Meta:
        model = Tag
        fields = ("name",)
