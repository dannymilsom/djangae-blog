from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'col-xs-12',
                'title': 'Username',

            }),
            'password': forms.TextInput(attrs={
                'placeholder': 'Password',
                'class': 'col-xs-12',
                'title': 'Password',
            }),
        }