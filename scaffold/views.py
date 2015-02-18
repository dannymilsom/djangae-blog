from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from google.appengine.api import users

from scaffold.utils import build_query

from blog.models import Article

def search(request):
    """Search the Datastore for query string matches."""

    data = {}
    # searching the content raises an exception using a Datastore backend
    fields = ('title', 'slug')
    query_string = request.GET.get('search', '').strip()
    data['query'] = query_string

    if query_string:
        entry_query = build_query(query_string, fields)
        data['articles'] = Article.objects.filter(entry_query)

    return render(request, 'search.html', data)

def login(request):
    """Redirects to the Google App Engine authentication page."""

    url = users.create_login_url(dest_url=request.GET.get('next'))
    return HttpResponseRedirect(url)

def logout(requesr):
    """Redirects to the homepage after logging the user out."""

    url = users.create_logout_url(reverse('home'))
    return HttpResponseRedirect(url)