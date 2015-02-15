from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
# import session_csrf
# session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

from rest_framework import routers
router = routers.DefaultRouter()
from blog.api import ArticleViewSet
router.register(r'articles', ArticleViewSet)

urlpatterns = patterns('',
    url(r'^$',  TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^_ah/', include('djangae.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'^feed/$', 'blog.views.feed', name='feed'),
    url(r'^login/$', 'scaffold.views.login', name='login'),
    url(r'^logout/$', 'scaffold.views.logout', name='logout'),
    url(r'^search/$', 'scaffold.views.search', name='search'),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
