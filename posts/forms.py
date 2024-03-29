from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'group': ('Группа'),
            'text': ('Текст'),
            'image': ('Картинка'),
        }
        help_texts = {
            'text': 'Введите текст ',
            'group': 'Укажите группу',
            'image': 'Добавьте картинку',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
