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

    def clean_subject(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Вы должны заполнить это поле')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
