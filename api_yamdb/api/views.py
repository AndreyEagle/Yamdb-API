from rest_framework import viewsets
from api.permissions import AuthorOrReadOnly
from rest_framework.generics import get_object_or_404

from api.serializers import (
    CommentsSerializer,
    ReviewSerializer)
from reviews.models import Comments, Review


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
    """
    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Title, id=title_id)
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset"""

    def perform_create(self, serializer):
        # title_id = self.kwargs.get("title_id")
        # title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, id=review_id)
        new_queryset = Comments.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
