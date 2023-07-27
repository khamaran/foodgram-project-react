from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from foodgram.constants import NAME_MAX_LENGTH, EMAIL_MAX_LENGTH


class MyUser(AbstractUser):
    """Кастомная модель `User`."""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )
    USER = 'user'
    ADMIN = 'admin'
    ROLES_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(_('Электронная почта'),
                              max_length=EMAIL_MAX_LENGTH, unique=True)
    username = models.CharField(
        verbose_name='Юзернейм',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(), ),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=NAME_MAX_LENGTH,
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=NAME_MAX_LENGTH,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель Подписки."""
    follower = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='following',
        verbose_name='Автор')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_follow',
            )
        ]

    def __str__(self):
        return f'Пользователь {self.follower} подписался на {self.following}'
