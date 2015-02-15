from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    """Defines a single blog entry which we refer to as an Article."""

    class Meta:
        ordering = ['-created_at']

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.URLField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog.views.display_article',
                       kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    """Defines a comment in response to an Article object."""

    class Meta:
        ordering = ['-created_at']

    article = models.ForeignKey(Article)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
