from rest_framework import serializers

from rest_framework_serializer_mixins import DynamicFieldsMixin

from .models import Post


class DynamicPostSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'body',
            'created_at',
            'id',
            'title',
            'updated_at',
            'user',
        )
        read_only_fields = (
            'id',
            'user',
        )
