from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls.base import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Nikita')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                description='Тестовое описание',
                slug='test-slug',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст потса',
            pub_date='2020-12-15',
            author=cls.user,
            group=cls.group,
        )
        cls.authorized_client_1 = Client()
        cls.user_1 = User.objects.create(username='Alena')
        cls.authorized_client_1.force_login(cls.user_1)
        cls.post_1 = Post.objects.create(
            text='Тестовый текст потса 1',
            author=cls.user_1,
        )

    def test_authorized_client(self):
        pages = {
            reverse('index'): 200,
            reverse('post_new'): 200,
            reverse('group_posts', args=[self.group.slug]): 200,
            reverse('profile', args=[self.user]): 200,
            reverse('post', args=[self.user.username, self.post.id]): 200,
            reverse(
                'post_edit', args=[self.user.username, self.post.id]
            ): 200,
            reverse('500'): 500,
            '/none/&/&/none/': 404,
            reverse(
                'add_comment', args=[self.user.username, self.post.id]
            ): 302,
            reverse('profile_follow', args=[self.user]): 302,
            reverse('profile_unfollow', args=[self.user]): 302
        }
        for url, status in pages.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_client(self):
        pages = {
            reverse('index'): 200,
            reverse('post_new'): 302,
            reverse('group_posts', args=[self.group.slug]): 200,
            reverse('profile', args=[self.user]): 200,
            reverse('post', args=[self.user, self.post.id]): 200,
            reverse('post_edit', args=[self.user, self.post.id]): 302,
            reverse('500'): 500,
            '/none/&/&/none/': 404,
            reverse(
                'add_comment', args=[self.user.username, self.post.id]
            ): 302,
        }
        for url, status in pages.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect(self):
        pages = {
            'post_new': reverse('post_new'),
            'post_edit': reverse(
                            'post_edit', args=[self.user, self.post.id]
                         ),
            'add_comment': reverse(
                            'add_comment', args=[self.user, self.post.id])
        }
        for names, url in pages.items():
            with self.subTest(names=names):
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, reverse('login')+'?next='+url)

    def test_post_edit_authorized_user_not_the_author(self):
        response = self.authorized_client_1.get(
            reverse('post_edit',
                    kwargs={'username': self.user, 'post_id': self.post.id}),
            follow=True)
        self.assertRedirects(
            response, reverse('post', args=[self.user, self.post.id])
        )

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            reverse('index'): 'posts/index.html',
            reverse('post_new'): 'posts/post_new.html',
            reverse('group_posts', args=[self.group.slug]): 'group.html',
            reverse('profile', args=[self.user]): 'posts/profile.html',
            reverse('post', args=[self.user, self.post.id]): 'posts/post.html',
            reverse(
                'post_edit', args=[self.user, self.post.id]
            ): 'posts/post_new.html',
            reverse('500'): 'misc/500.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
