import random

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from .permissions import IsAdmin
from .serializers import (SignUpSerializer, TokenSerializer, UserMeSerializer,
                          UserSerializer)


class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserMeSerializer
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if self.request.method == 'PATCH':
            self.partial_update(request)
            request.user.refresh_from_db()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class SignUpViewSet(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    confirmation_code = str(random.randint(10000, 99999))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def perform_create(self, serializer):
        EmailMessage(
            'Confirmation_code',
            f'Ваш confirmation_code {self.confirmation_code}',
            'Yamdb@yamdb.com',
            (serializer.validated_data['email'],)
        ).send()
        serializer.save(
            confirmation_code=self.confirmation_code,
        )


class TokenViewSet(generics.CreateAPIView):
    serializer_class = TokenSerializer

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        response = get_tokens_for_user(user)
        return Response(response, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    access = AccessToken.for_user(user)
    return {'token': str(access)}
