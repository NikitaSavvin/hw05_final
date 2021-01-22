from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

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
            pub_date='2020-12-15',
            author=cls.user,
            group=cls.group,
            image=cls.test_image
        )
        cls.group_1 = Group.objects.create(
            title='test-group-1',
            slug='test-slug-1',
            description='Tестовое описание 1',
        )
        cls.user_1 = User.objects.create(username='Alena')

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('index'): 'posts/index.html',
            reverse('post_new'): 'posts/post_new.html',
            reverse('group_posts', args=[self.group.slug]): 'group.html',
            reverse('profile', args=[self.post.author]): 'posts/profile.html',
            reverse(
                'post_edit', args=[self.post.author, self.post.id]
            ): 'posts/post_new.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_correct_context(self):
        list_of_pages = (
            reverse('index'),
            reverse('group_posts', args=[self.group.slug]),
            reverse('post', args=[self.user.username, self.post.id]),
            reverse('profile', args=[self.user.username]),
        )
        for reverse_name in list_of_pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                paginator = response.context.get('paginator')
                if paginator is not None and paginator.count == 1:
                    post_n = response.context['page'][0]
                else:
                    post_n = response.context['post']
                post_text_0 = post_n.text
                post_author_0 = post_n.author
                pub_date_0 = post_n.pub_date
                post_group_0 = post_n.group
                post_image_0 = post_n.image
                self.assertEqual(post_text_0, self.post.text)
                self.assertEqual(post_author_0, self.post.author)
                self.assertEqual(pub_date_0, self.post.pub_date)
                self.assertEqual(post_group_0, self.post.group)
                self.assertEqual(post_image_0, self.post.image)

    def test_forms_new_and_edit(self):
        urls = [
            reverse('post_new'),
            reverse(
                'post_edit',
                args=[self.user, self.post.id]
            )
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            #'image': forms.fields.ImageField,
        }
        for url in urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                for value, expected in form_fields.items():
                    form_field = response.context['form'].fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_post_not_in_group_off(self):
        response = self.authorized_client.get(
            reverse('group_posts', args=[self.group_1.slug])
        )
        response_posts = response.context.get('page')
        self.assertEqual(response_posts.object_list.count(), 0)

    def test_post_in_pages(self):
        pages = {
            'index': reverse('index'),
            'group_posts': reverse('group_posts', args=[self.group.slug])
        }
        for names, slugs in pages.items():
            with self.subTest(names=names):
                response = self.authorized_client.get(slugs)
                self.assertEqual((response.context.get('paginator').count), 1)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create(
            username='Nikita'
        )
        cls.group = Group.objects.create(
                title='Тестовый заголовок',
                slug='test-slug',
        )
        for i in range(0, 13):
            Post.objects.create(
                text=f'Тестовый текст потса {i}',
                author=PaginatorViewTest.user,
                group=PaginatorViewTest.group
            )

    def test_first_page_containse_ten_records(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context.get('page').object_list), 10)

    def test_second_page_containse_three_records(self):
        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(len(response.context.get('page').object_list), 3)

    def test_page_contains_thirteen(self):
        response = self.client.get(reverse('index'))
        self.assertEqual((response.context.get('paginator').count), 13)
 