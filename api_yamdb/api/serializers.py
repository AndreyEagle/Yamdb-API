from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        model = User
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
            ),
        )


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
            ),
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )
    email = serializers.EmailField(
        max_length=254,
        validators=(UniqueValidator(queryset=User.objects.all()),)
    )

    class Meta:
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message='Поля username и email обязательны для заполнения'
            ),
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовать это имя в качестве username запрещено.')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = user.confirmation_code
        if data['confirmation_code'] != confirmation_code:
            raise serializers.ValidationError('Неверный confirmation_code')
        return data
