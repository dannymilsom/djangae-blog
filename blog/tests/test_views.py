from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User = get_user_model()

from google.appengine.ext import testbed

from blog.models import Article

class ArticleViewsTest(TestCase):

    article_data = (
        {
            'title': 'Blog Post One',
            'image': 'www.example.com/example.jpg',
            'content': 'Hello World!',
        },
        {
            'title': 'Blog Post Two',
            'image': 'www.example.com/example2.jpg',
            'content': 'Hello again!',
        },
        {
            'title': 'Blog Post Three',
            'image': 'www.example.com/image3.jpg',
            'content': 'Bonjour',
        }
    )

    def setUp(self):
        """Initalise GAE test stubs before each test is run."""

        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        """Remove the GAE test subs after each test."""
        self.testbed.deactivate()

    def user_login(self):
        """
        Set user environment variables and initalise the GAE user stub.

        Taken from http://stackoverflow.com/questions/6159396/.
        """

        self.testbed.setup_env(
            USER_EMAIL='admin@example.com',
            USER_ID='12345',
            USER_IS_ADMIN='1',
            overwrite=True,
        )
        self.testbed.init_user_stub()

    def create_articles(self):
        test_user = User.objects.pre_create_google_user(email='test@example.com')
        for article in self.article_data[:2]:
            article.update({'author': test_user})
            Article.objects.create(**article)

    def test_display_all_articles(self):
        self.create_articles()
        response = self.client.get(reverse('display_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/articles.html')
        self.assertEqual(len(response.context['articles']), 2)

    def test_display_limited_articles(self):
        self.create_articles()
        response = self.client.get("%s?limit=1" % reverse('display_articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/articles.html')
        self.assertEqual(len(response.context['articles']), 1)

    def test_display_specific_article(self):
        self.create_articles()
        response = self.client.get(reverse('display_article',
                kwargs={'slug': 'blog-post-one'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article.html')
        self.assertTrue('article' in response.context)

    def test_article_does_not_exist(self):
        self.create_articles()
        response = self.client.get(reverse('display_article',
                kwargs={'slug': 'foo-bar'}))
        self.assertEqual(response.status_code, 404)

    def test_create_article_redirects_anonymous(self):
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 302)

    def test_create_article_allows_authenticated(self):
        self.user_login()
        response = self.client.get(reverse('create_article'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_or_edit_article.html')
        self.assertTrue('form' in response.context)

    def test_create_articles_valid(self):
        self.user_login()
        response = self.client.post(reverse('create_article'),
                self.article_data[2])
        self.assertEqual(Article.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_edit_article_redirects_anonymous(self):
        response = self.client.get(reverse('edit_article',
                kwargs={'slug': 'foo-bar'}))
        self.assertEqual(response.status_code, 302)

    def test_edit_article_allows_authenticated(self):
        self.create_articles()
        self.user_login()
        response = self.client.get(reverse('edit_article',
                kwargs={'slug': 'blog-post-one'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/create_or_edit_article.html')
        self.assertTrue('form' in response.context)

    def test_delete_article_redirects_anonymous(self):
        response = self.client.get(reverse('delete_article',
                kwargs={'slug': 'blog-post-one'}))
        self.assertEqual(response.status_code, 302)

    def test_delete_article_allows_authenticated(self):
        self.create_articles()
        self.user_login()
        response = self.client.get(reverse('delete_article',
                kwargs={'slug': 'blog-post-one'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/delete_article.html')
        self.assertTrue('form' in response.context)

    def test_delete_articles_valid(self):
        self.create_articles()
        self.assertEqual(Article.objects.all().count(), 2)
        self.user_login()
        response = self.client.post(reverse('delete_article',
                kwargs={'slug': 'blog-post-one'}))
        self.assertEqual(Article.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_admin_home_redirects_anonymous(self):
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

    def test_admin_home_allows_authenticated(self):
        self.create_articles()
        self.user_login()
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/admin_home.html')
        self.assertTrue('articles' in response.context)

    def test_feed_view(self):
        self.create_articles()
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/feed.html')
