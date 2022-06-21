from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from Account.models import Account
from .models import Post, Like
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = 'blogs/feed.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostLikeView(View):

    def post(self,request,*args,**kwargs):
        user = self.request.user
        print(user)
        pk = kwargs['pk']
        print(kwargs)
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            print(post_id)
            post_obj = Post.objects.get(id=post_id)
            profile = Account.objects.get(user=user)

            if profile in post_obj.liked.all():
                post_obj.liked.remove(profile)
            else:
                post_obj.liked.add(profile)

            like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

            if not created:
                if like.value == 'Like':
                    like.value = 'Unlike'
                else:
                    like.value = 'Like'

                post_obj.save()
                like.save()
        return redirect('blog-post', pk=pk)

# def like_unlike_view(request, *args, **kwargs):
#     user = request.user
#     print(user)
#     pk = kwargs['pk']
#     print(kwargs)
#     if request.method == 'POST':
#         post_id = request.POST.get('post_id')
#         print(post_id)
#         post_obj = Post.objects.get(id=post_id)
#         profile = Account.objects.get(user=user)
#
#         if profile in post_obj.liked.all():
#             post_obj.liked.remove(profile)
#         else:
#             post_obj.liked.add(profile)
#
#         like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
#
#         if not created:
#             if like.value == 'Like':
#                 like.value = 'Unlike'
#             else:
#                 like.value = 'Like'
#
#             post_obj.save()
#             like.save()
#     return redirect('blog-post', pk=pk)


