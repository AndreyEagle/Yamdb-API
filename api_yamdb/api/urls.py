from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet, 
                       CommentsViewSet, ReviewViewSet)


router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
