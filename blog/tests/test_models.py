from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from blog.models import Article, Comment

from google.appengine.ext import testbed

class ArticleModelTest(TestCase):

    def setUp(self):
        """Initalise GAE test stubs before each test is run."""
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        test_user = User.objects.pre_create_google_user(email='test@example.com')
        self.article_data = {
            'title': 'Blog Post One',
            'author': test_user,
            'image': 'www.example.com/example.jpg',
            'content': 'Hello World!',
        }

    def tearDown(self):
        """Remove the GAE test subs after each test."""
        self.testbed.deactivate()

        test_user = User.objects.pre_create_google_user(email='test@example.com')
        self.article_data = {
            'title': 'Blog Post One',
            'author': test_user,
            'image': 'www.example.com/example.jpg',
            'content': 'Hello World!',
        }

    def create_article(self, **kwargs):
        return Article.objects.create(**kwargs)

    def test_article_creation(self):
        article = self.create_article(**self.article_data)
        self.assertTrue(isinstance(article, Article))
        self.assertEqual(article.__unicode__(), article.title)
        self.assertEqual(article.get_absolute_url(),
            reverse('blog.views.display_article',
                    kwargs={'slug': article.slug}))


class CommentModelTest(TestCase):

    def setUp(self):
        """Initalise GAE test stubs before each test is run."""
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        test_user = User.objects.pre_create_google_user(email='test@example.com')
        self.article_data = {
            'title': 'Blog Post One',
            'author': test_user,
            'image': 'www.example.com/example.jpg',
            'content': 'Hello World!',
        }

        self.comment_data = {
            'article': Article.objects.create(**self.article_data),
            'name': 'John Cleese',
            'email': 'johncleese@example.com',
            'message': 'This is an ex-parrot!',
        }

        Article.objects.create(**self.article_data)

    def create_comment(self, **kwargs):
        return Comment.objects.create(**kwargs)

    def test_comment_creation(self):
        """
        Currently fails with DataError: Unable to acquire marker for 
        blog_article|slug.
        """

        comment = self.create_comment(**self.comment_data)
        self.assertTrue(isinstance(comment, Comment))
        self.assertEqual(comment.__unicode__(), comment.message)
