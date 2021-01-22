from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostFormModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-group',

        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            author=User.objects.create(username='testuser'),
            group=cls.group
        )

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='Nikita')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_verbose_name_group(self):
        group = PostFormModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Адрес для страницы с группой',
            'description': 'Описание',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected
                )

    def test_verbose_name_post(self):
        post = PostFormModelTest.post
        field_verboses = {
            'text': 'Текст',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        group = PostFormModelTest.group
        post = PostFormModelTest.post
        field_help_texts = {
            'title': 'Заголовок группы',
            'slug': (
                     'Укажите адрес для страницы группы. Используйте только '
                     'латиницу, цифры, дефисы и знаки подчёркивания'
                     ),
            'description': 'Дайте описание группы',
            'text': 'Напишите текст поста',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                if value == 'text':
                    post._meta.get_field(value).help_text, expected
                else:
                    group._meta.get_field(value).help_text, expected

    def test_object_text_len_field(self):
        post = self.post
        group = self.group
        expected_text = {
            post: self.post.text[:15],
            group: self.group.title
        }
        for model, status in expected_text.items():
            with self.subTest(model=model):
                self.assertEqual(status, str(model))
