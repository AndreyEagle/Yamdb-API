from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


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
