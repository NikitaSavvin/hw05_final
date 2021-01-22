# Generated by Django 3.1.4 on 2020-12-30 17:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Заголовок группы', max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(help_text='Укажите адрес для страницы группы. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', max_length=200, unique=True, verbose_name='Адрес для страницы с группой')),
                ('description', models.TextField(help_text='Дайте описание группы', verbose_name='Описание')),
                ('name_group', models.TextField(help_text='Дайте название вашей группе', max_length=200, verbose_name='Название группы')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Напишите текст поста', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата публикации', verbose_name='date published')),
                ('author', models.ForeignKey(help_text='Имя автора', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(blank=True, help_text='Тест группа', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='posts.group')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
    ]
