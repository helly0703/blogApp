from django.urls import path
from .views import (
    HomeView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostLikeView,
    PostCommentCreateView,
    SavedPostListView,
    PostSaveView,
    PostFilterView,
    CategoryListView,
    SearchBlogView
)


urlpatterns = [
    path('', HomeView.as_view(), name="blogs"),

    path('blogpost/search/', SearchBlogView.as_view(), name="search_post"),
    path('blogpost/new/', PostCreateView.as_view(), name="post-create"),
    path('blogpost/<int:pk>/', PostDetailView.as_view(), name="blog-post"),
    path('blogpost/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blogpost/filter/', CategoryListView.as_view(), name='filter-blog'),
    path('blogpost/filter-posts/', PostFilterView.as_view(), name='category-list'),
    path('blogpost/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('blogpost/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blogpost/<int:pk>/comment/', PostCommentCreateView.as_view(), name='post-comment'),
    path('blogpost/saved', SavedPostListView.as_view(), name='post-saved'),
    path('blogpost/save-post/', PostSaveView.as_view(), name='save-post'),

]
