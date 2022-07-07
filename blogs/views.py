from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from Account.models import Account
from .forms import BlogCreateForm
from .models import Post, Like, Comment, SavePost, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    paginate_by = 2
    model = Post
    template_name = 'blogs/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data()
        posts = Post.objects.filter(
            Q(author__in=self.request.user.account.friendslist.all()) | Q(author=self.request.user)).order_by(
            '-date_posted')
        paginator = Paginator(posts, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        context['posts'] = post_list
        context['categories'] = Category.objects.all()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = BlogCreateForm
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        print(f"FORM {form.data}")
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = BlogCreateForm
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form)

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


class PostLikeView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # pk = kwargs['pk']
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
                msg = like.value

                post_obj.save()
                like.save()
        return HttpResponse(msg)


class PostCommentCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = self.request.user
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            print(post_id)
            comment = request.POST.getlist('comment')
            print(comment)
            profile = Account.objects.get(user=user)
            Comment.objects.get_or_create(user=profile, post_id=post_id, body=comment[0])
            msg='Success'
        return HttpResponse(msg)


class PostCommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'blogs/feed.html'

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        print(pk)
        queryset = super().get_queryset()
        return queryset.filter(post_id=pk)


class SavedPostListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = 'blogs/saved_blogs.html'
    context_object_name = 'qs'

    def get_queryset(self, **kwargs):
        saved = SavePost.objects.filter(user=self.request.user.account, value='Save')
        print(saved)
        qs = []
        for item in saved:
            if item.post.author in self.request.user.account.friendslist.all() or item.post.author == self.request.user:
                qs.append(Post.objects.get(title=item.post))
        print(qs)

        return qs


class PostSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            print(post_id)
            post_obj = Post.objects.get(id=post_id)
            profile = Account.objects.get(user=user)
            if profile in post_obj.saved.all():
                post_obj.saved.remove(profile)
            else:
                post_obj.saved.add(profile)

            saved, created = SavePost.objects.get_or_create(user=profile, post=post_obj, value='Save')
            print(saved.value)
            if not created:
                if saved.value == 'Save':
                    msg='Save'
                    saved.value = 'Unsave'
                else:
                    msg='Unsave'
                    saved.value = 'Save'

            print(saved.value)
            if saved.value == 'Save':
                msg = 'Unsave'
            elif saved.value == 'Unsave':
                msg = 'Save'

            post_obj.save()
            saved.save()
        return HttpResponse(msg)


class PostFilterView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = "blogs/feed.html"


    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get("category-id")
        posts = Post.objects.filter(category=query)
        qs = []
        for item in posts:
            if item.author in self.request.user.account.friendslist.all() or item.author == self.request.user:
                qs.append(Post.objects.get(title=item))
        context = super(PostFilterView, self).get_context_data()
        context['posts'] = qs
        context['categories'] = Category.objects.all()
        print(context)
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "blogs/filter.html"
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Category.objects.filter()
        return qs

