from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpViewSet, TokenViewSet, UserViewSet

app_name = 'reviews'
app_name = 'api'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpViewSet.as_view()),
    path('v1/auth/token/', TokenViewSet.as_view()),
]
