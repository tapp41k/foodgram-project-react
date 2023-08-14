from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    """Класс пользователей."""

    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
        db_index=True
    )
    username = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=(UnicodeUsernameValidator(), validate_username)
    )
    first_name = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='имя'
    )
    last_name = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_USER,
        verbose_name='фамилия'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:settings.LENGTH_TEXT]


class Subscription(models.Model):
    """Класс для подписки на авторов контента."""

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'subscriber'),
                name='unique_subscription'
            ),
        )

    def __str__(self):
        return f'{self.subscriber} подписан на: {self.author}'
