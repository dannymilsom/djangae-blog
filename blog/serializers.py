from rest_framework import serializers

from blog.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """Model Serializer for the Article model."""
    
    created_at = serializers.DateTimeField(format='%F')
    author = serializers.StringRelatedField()
    class Meta:
        model = Article
        fields = ('title', 'content', 'image', 'slug', 'author', 'created_at')