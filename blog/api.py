from rest_framework import viewsets

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
