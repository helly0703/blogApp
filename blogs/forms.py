from django import forms

from blogs.models import Post


class BlogCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
