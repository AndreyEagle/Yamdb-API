from reviews.models import Category, Genre, Title, Review, Comments
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from .serializers import (CategorySerializer,
                          GenreSerializer, TitleCreateSerializer,
                          TitleSerializer, CommentsSerializer,
                          ReviewSerializer)
from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


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

