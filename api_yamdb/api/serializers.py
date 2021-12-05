from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comments, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'title',)
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Comments
