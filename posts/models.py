from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
        help_text='Заголовок группы'
    )
    slug = models.SlugField(
        'Адрес для страницы с группой',
        max_length=200,
        unique=True,
        help_text=(
            'Укажите адрес для страницы группы. Используйте только '
            'латиницу, цифры, дефисы и знаки подчёркивания'
        )
    )
    description = models.TextField(
        'Описание',
        help_text=('Дайте описание группы')
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст',
        help_text='Напишите текст поста'
    )
    pub_date = models.DateTimeField(
        "Дата публикации", 
        auto_now_add=True, 
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Имя автора'
    )
    group = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Тест группа'
    )
    image = models.ImageField(
        upload_to='posts/', blank=True, null=True
    )  
    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Тест группа'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Имя автора'
    )
    text = models.TextField(
        'Текст',
        help_text='Напишите текст коментария',
    )
    created = models.DateTimeField(
        'date published',
        auto_now_add=True,
        help_text='Дата публикации',
    )



class Follow(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User, null=True,
        on_delete=models.CASCADE,
        related_name='following'
    )