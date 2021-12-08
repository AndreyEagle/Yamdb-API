from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    year = models.IntegerField(verbose_name='Год создания')

    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Описание'
    )

    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(0), ])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', null=True)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True, null=True)


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True, null=True)
