from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MinLengthValidator, RegexValidator, ValidationError)
from django.db.models import PROTECT, CASCADE
import json
import os

# Create your models here.
class User(AbstractUser):
    boards = models.ManyToManyField("Board", related_name="boards")
    avatar = models.ImageField(upload_to="avatars/", null=True,
                               blank=True, verbose_name="Аватар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # JSON поле для настроек
    settings = models.JSONField(default=dict, blank=True, verbose_name='Настройки')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        db_table = 'users'

class Board(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название доски", db_index=True)
    description = models.TextField(max_length=200, blank=True, verbose_name="Описание доски")
    is_private = models.BooleanField(default=False, verbose_name="Секретная")

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"
        db_table = 'boards'

    def __str__(self):
        return self.title

class Pin(models.Model):
    boards = models.ManyToManyField(Board, related_name="pins")
    title = models.CharField(max_length=50, verbose_name="Название поста",
                             db_index=True)
    liked_by = models.ManyToManyField(User, related_name="likes", verbose_name="Лайки")
    description = models.TextField(max_length=200, blank=True,
                                   verbose_name="Описание")
    content = models.FileField(upload_to="uploads/", blank=True, null=True,
                               verbose_name="Контент")
    user = models.ForeignKey(User, on_delete=PROTECT, verbose_name="Пользователь",
                             related_name="pins")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Отредактировано")
    is_private = models.BooleanField(default=False, verbose_name="Секретный")

    def is_video(self):
        # Список видео-расширений
        video_extensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
        ext = os.path.splitext(self.content.name)[1].lower()
        return ext in video_extensions

    def is_image(self):
        # Список графических расширений
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
        ext = os.path.splitext(self.content.name)[1].lower()
        return ext in image_extensions

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if not(self.is_image() or self.is_video()):
            raise ValidationError({'content': 'Неподдерживаемый тип файла'})


class Comment(models.Model):
    content = models.TextField(max_length=200, verbose_name="Содержание сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Отредактировано")
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE, related_name='comments',
                             verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',
                               verbose_name="Пользователь")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        db_table = 'comments'
        ordering = ['-created_at']

    def __str__(self):
        return self.content

# class UserBoard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,
#                              verbose_name="Пользователь", related_name="user_boards", db_index=True)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE,
#                               verbose_name="Доска", related_name="user_boards", db_index=True)
#
#     class Meta:
#         db_table = 'user_board'
#         unique_together = ['user', 'board']  # Запрещаем дубликаты
#
#
# class PinBoard(models.Model):
#     pin = models.ForeignKey(Pin, on_delete=models.CASCADE,
#                             verbose_name="Пост", related_name="pin_boards", db_index=True)
#     board = models.ForeignKey(Board, on_delete=models.CASCADE,
#                               verbose_name="Доска", related_name="pin_boards", db_index=True)
#
#     class Meta:
#         db_table = 'pin_boards'
#         unique_together = ['pin', 'board']  # Запрещаем дубликаты