from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USERS_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    password = models.CharField(
        max_length=128,
        verbose_name='password',
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        blank=True,
        max_length=254,
        verbose_name='email address'
    )
    confirmation_code = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    role = models.CharField(
        'Пользовательские роли',
        max_length=16,
        choices=USERS_ROLE,
        default=USER,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=150,
        verbose_name='last name'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('username', 'email',),
                name='unique_user'
            ),
        )


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    pass


class Comments(models.Model):
    pass
