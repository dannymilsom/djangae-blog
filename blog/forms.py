from django import forms

from blog.models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'My Article Title',
                'class': 'col-xs-12 col-sm-offset-2 col-sm-8',
                'title': 'Article Title',
            }),
            'image': forms.TextInput(attrs={
                'placeholder': 'www.example.com/image.png',
                'class': 'col-xs-12 col-sm-offset-2 col-sm-8',
                'title': 'Image URL',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your content here...',
                'class': 'col-xs-12 col-sm-offset-2 col-sm-8',
                'title': 'Enter the article content here', 'rows': 10,
            }),
        }

class DeleteArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = []

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Danny',
                'class': 'col-xs-12 col-sm-6',
                'title': 'Name',
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'danny@example.com',
                'class': 'col-xs-12 col-sm-6',
                'title': 'Email address',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Love the blog post! Thanks.',
                'class': 'col-xs-12',
                'title': 'Enter you comments here', 'rows': 4,
            }),
        }
