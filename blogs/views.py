from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
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
# For displaying blogs in the feed
class HomeView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = 'blogs/feed.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data()
        public_accounts = Account.objects.filter(privacy_mode='PUBLIC')
        print(f'public accounts{public_accounts}')
        print(self.request.user.account.friendslist.all())
        # To display blogs were post author is friend or user
        posts = Post.objects.filter(
            Q(author__in=self.request.user.account.friendslist.all()) | Q(author=self.request.user) | Q(
                author__in=self.request.user.account.get_user_public())).order_by(
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


# Viewing individual post
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'


# For creating new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = BlogCreateForm
    success_url = reverse_lazy('blogs')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)


# For updating post if post author is user
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


# For deleting post if post author is user
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blogs')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


# To like-unlike posts
class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Account.objects.get(user=user)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
        # if liked then unlike post and vice versa
        msg=''
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
            msg = like.value

            post_obj.save()
            like.save()
        return HttpResponse(msg)


# To comment posts
class PostCommentCreateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.POST.get('post_id')
        comment = request.POST.getlist('comment')
        profile = Account.objects.get(user=user)
        Comment.objects.get_or_create(user=profile, post_id=post_id, body=comment[0])
        msg = 'Success'
        return HttpResponse(msg)


#  To view posts
class PostCommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'blogs/feed.html'

    def get_queryset(self, **kwargs):
        pk = kwargs['pk']
        queryset = super().get_queryset()
        return queryset.filter(post_id=pk)


# To view saved posts
class SavedPostListView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = 'blogs/saved_blogs.html'
    context_object_name = 'qs'

    def get_queryset(self, **kwargs):
        saved = SavePost.objects.filter(user=self.request.user.account, value='Save')
        qs = []
        for item in saved:
            qs.append(Post.objects.get(title=item.post))
        return qs


# To save-unsave posts
class PostSaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Account.objects.get(user=user)
        if profile in post_obj.saved.all():
            post_obj.saved.remove(profile)
        else:
            post_obj.saved.add(profile)

        saved, created = SavePost.objects.get_or_create(user=profile, post=post_obj, value='Save')
        if not created:
            if saved.value == 'Save':
                msg = 'Save'
                saved.value = 'Unsave'
            else:
                msg = 'Unsave'
                saved.value = 'Save'

        if saved.value == 'Save':
            msg = 'Unsave'
        elif saved.value == 'Unsave':
            msg = 'Save'

        post_obj.save()
        saved.save()
        return HttpResponse(msg)


# To filter posts by category
class PostFilterView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = "blogs/feed.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get("category-id")
        if query:
            #  filter by category
            qs = Post.objects.filter(category=query).filter(
                Q(author__in=self.request.user.account.friendslist.all()) | Q(author=self.request.user) | Q(
                    author__in=self.request.user.account.get_user_public())).order_by(
                '-date_posted')
        else:
            qs = Post.objects.filter(
                Q(author__in=self.request.user.account.friendslist.all()) | Q(author=self.request.user) | Q(
                    author__in=self.request.user.account.get_user_public())).order_by(
                '-date_posted')
        context = super(PostFilterView, self).get_context_data()
        context['posts'] = qs
        context['categories'] = Category.objects.all()
        context['selected_category'] = query
        return context


# View category
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "blogs/filter.html"
    context_object_name = 'qs'

    def get_queryset(self):
        qs = Category.objects.filter()
        return qs


class SearchBlogView(LoginRequiredMixin, ListView):
    paginate_by = 5
    model = Post
    template_name = "blogs/feed.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        query = self.request.GET.get("search_field")
        qs = Post.objects.filter(
            Q(title__icontains=query)
        ).filter(
            Q(author__in=self.request.user.account.friendslist.all()) | Q(author=self.request.user) | Q(
                author__in=self.request.user.account.get_user_public())).order_by(
            '-date_posted')
        context = super(SearchBlogView, self).get_context_data()
        context['posts'] = qs
        context['categories'] = Category.objects.all()
        return context

