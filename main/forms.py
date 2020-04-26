from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User, Post


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     initial = kwargs.get('initial', None)
    #     if initial:
    #         product = initial.get('product', None)
    #     else:
    #         product = None
    #     super().__init__(*args, **kwargs)