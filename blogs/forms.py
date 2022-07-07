from django import forms
from blogs.models import Post, Category


class BlogCreateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        choices = Category.objects.all().values_list('name', 'name')
        choice_list = []
        for item in choices:
            choice_list.append(item)

        model = Post
        fields = ['title', 'content', 'image', 'category']

        widgets = {
            'category': forms.Select(choices=choice_list,attrs={'class': 'form-control'}),
        }
