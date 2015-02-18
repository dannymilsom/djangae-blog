from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from blog.forms import ArticleForm, DeleteArticleForm, CommentForm
from blog.models import Article, Comment

def display_article(request, slug):
    """
    Renders a template to display a single Article, identified by its slug.

    If no Article object matches the slug request, we return 404.
    """

    article = get_object_or_404(Article, slug=slug)

    form = CommentForm(request.POST or None, instance=Comment())
    if request.method == 'POST' and form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.article = article
        new_comment.save()
        return HttpResponseRedirect(reverse('display_article',
                kwargs={'slug': article.slug}))

    data = {
        'article': article,
        'comments': Comment.objects.filter(article=article),
        'form': form,
    }

    return render(request, 'blog/article.html', data)

def display_articles(request, limit=None):
    """
    Renders a template to display multiple Article objects.

    If a limit GET parameter is passed, the number of Article objects 
    returned will be restricted to satisfy this condition.
    """

    limit = request.GET.get('limit')
    articles = Article.objects.all()
    if limit:
        try:
            article_limit = int(limit)
        except ValueError:
            return render(request, 'error.html', {'article_limit': limit})
        else:
            articles = articles[:article_limit]

    return render(request, 'blog/articles.html', {'articles': articles})

@login_required()
def create_or_edit_article(request, slug=None):
    """
    Renders a form to support the creation of new article objects, and the 
    modification of an existing article object.

    If a new article is successfully created, the response is redirected 
    to a preview of that article.
    """

    if slug:
        article = get_object_or_404(Article, slug=slug)
    else:
        article = Article()

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return HttpResponseRedirect(reverse('display_article',
                    kwargs={'slug': new_article.slug}))
    else:
        form = ArticleForm(instance=article)

    data = {'form': form}
    return render(request, 'blog/create_or_edit_article.html', data)

@login_required()
def delete_article(request, slug):
    """
    Renders a form to support the deletion of existing article objects.

    Using a form allows us to protect against CSRF attacks.
    """

    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        form = DeleteArticleForm(request.POST, instance=article)
        if form.is_valid():
            article.delete()
            return HttpResponseRedirect(reverse('display_articles'))
    else:
        form = DeleteArticleForm(instance=article)

    data = {'form': form}
    return render(request, 'blog/delete_article.html', data)

@login_required
def admin_home(request):
    """Renders a custom admin interface, with CRUD support for Articles."""

    data = {'articles': Article.objects.all()}
    return render(request, 'blog/admin_home.html', data)

def feed(request):
    """Displays articles using Backbone and the RESTful API."""

    return render(request, 'blog/feed.html', {})