from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Nikita')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-group',
        )
        cls.image_bytes = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.test_image = SimpleUploadedFile(
            name='test_image.gif',
            content=cls.image_bytes,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            author=cls.user,
            group=cls.group,
            image=cls.test_image,
        )
        cls.group_2 = Group.objects.create(
            title="Тестовый заголовок 2",
            slug="test-group_2",
            description="Тестовое описание_2",
        )

    def test_create_post_form(self):
        post_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'текст',
            'image': self.test_image,
        }
        response = self.authorized_client.post(
            reverse('post_new'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), post_count+1)
        created_post = Post.objects.exclude(id=self.post.id)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(created_post.text, form_data['text'])
        self.assertEqual(created_post.group.id, form_data['group'])
        self.assertEqual(self.user, self.post.author)
        self.assertTrue(self.post.image)

    def test_edit_post(self):
        post_count = Post.objects.count()
        form_data = {
            'group': self.group_2.id,
            'text': 'Измененный текст',
        }
        response = self.authorized_client.post(
            reverse(
                'post_edit', args=[self.post.author, self.post.id]
            ),
            data=form_data, follow=True
        )
        post_edit = response.context['post']
        self.assertEqual(Post.objects.count(), post_count)
        self.assertEqual(post_edit.text, form_data['text'])
        self.assertEqual(post_edit.group, self.group_2)
        self.assertEqual(post_edit.author, self.user)
