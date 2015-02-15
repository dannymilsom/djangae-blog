from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.forms import ArticleForm, CommentForm
from blog.models import Article

User = get_user_model()

class ArticleFormTest(TestCase):

    form_data = {
        'title': 'Blog Post One',
        'image': 'http://www.example.com/example.jpg',
        'content': 'Hello World!',
    }

    def test_valid_data(self):
        form = ArticleForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        article = form.save(commit=False)
        article.author = User.objects.create(username='admin',
                                             email='admin@example.com',
                                             password='pass')
        article.save()
        self.assertEqual(article.title, self.form_data['title'])
        self.assertEqual(article.image, self.form_data['image'])
        self.assertEqual(article.content, self.form_data['content'])

    def test_blank_data(self):
        form = ArticleForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors, {
            'title': ['This field is required.'],
            'image': ['This field is required.'],
            'content': ['This field is required.']
        })

class CommentFormTest(TestCase):

    def setUp(self):
        self.form_data = {
            'name': 'Joe Bloggs',
            'email': 'joe@example.com',
            'message': 'Really enjoyed this article - thanks!',
        }

    def test_valid_data(self):
        form = CommentForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        test_user = User.objects.create_user(username='admin',
                                             email='admin@example.com',
                                             password='pass')
        comment = form.save(commit=False)
        comment.article = Article.objects.create(
            title='Blog Post One',
            author=test_user,
            image='www.example.com/example.jpg',
            content='Hello World!')
        comment.save()
        self.assertEqual(comment.name, self.form_data['name'])
        self.assertEqual(comment.email, self.form_data['email'])
        self.assertEqual(comment.message, self.form_data['message'])

    def test_blank_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'message': ['This field is required.']
        })
