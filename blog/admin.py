from django.contrib import admin
from blog.models import Article, Comment

admin.site.register((Article, Comment))
