from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from Account.models import Account
from .models import Post, Like, Comment, SavePost
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


# Create your views here.
class HomeView(LoginRequiredMixin,ListView):
    # paginate_by = 2
    model = Post
    template_name = 'blogs/feed.html'


class PostDetailView(LoginRequiredMixin,DetailView):
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


class PostLikeView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        user = self.request.user
        pk = kwargs['pk']
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
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


class PostCommentCreateView(LoginRequiredMixin,View):

    def post(self,request,*args,**kwargs):
        pk = kwargs['pk']
        user = self.request.user
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            comment = request.POST.getlist("comment")
            profile = Account.objects.get(user=user)
            Comment.objects.get_or_create(user=profile, post_id=post_id,body =comment[0])
        return redirect('blog-post', pk=pk)


class PostCommentListView(LoginRequiredMixin,ListView):
    model = Comment
    template_name = 'blogs/feed.html'

    def get_queryset(self,**kwargs):
        pk = kwargs['pk']
        print(pk)
        queryset = super().get_queryset()
        return queryset.filter(post_id=pk)


class SavedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blogs/saved_blogs.html'
    context_object_name = 'qs'

    def get_queryset(self, **kwargs):
        saved = SavePost.objects.filter(user=self.request.user.account)
        print(saved)
        qs = []
        for item in saved:
            qs.append(Post.objects.get(title=item.post))
        print(qs)
        return qs


class PostSaveView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        user = self.request.user
        print(user)
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            post_obj = Post.objects.get(id=post_id)
            profile = Account.objects.get(user=user)
            if profile in post_obj.saved.all():
                post_obj.saved.remove(profile)
            else:
                post_obj.saved.add(profile)

            saved, created = SavePost.objects.get_or_create(user=profile, post=post_obj)

            if not created:
                if saved.value == 'Save':
                    saved.value = 'Unsave'
                else:
                    saved.value = 'Save'

        post_obj.save()
        saved.save()
        return redirect(request.META.get('HTTP_REFERER'))



