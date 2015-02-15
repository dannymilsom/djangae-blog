from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
    url(r'^$', 'display_articles', name='display_articles'),
    url(r'^admin/create-article$', 'create_or_edit_article', name='create_article'),
    url(r'^admin/edit-article/(?P<slug>[-a-zA-Z0-9]+)$', 'create_or_edit_article', name='edit_article'),
    url(r'^admin/delete-article/(?P<slug>[-a-zA-Z0-9]+)$', 'delete_article', name='delete_article'),
    url(r'^admin$', 'admin_home', name='admin_home'),
    url(r'^(?P<slug>[-a-zA-Z0-9]+)$', 'display_article', name='display_article'),
)
