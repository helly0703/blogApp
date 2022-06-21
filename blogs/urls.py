
from django.urls import path
from .views import HomeView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,PostLikeView


urlpatterns = [
    path('', HomeView.as_view(), name="blogs"),
    path('blogpost/new/', PostCreateView.as_view(), name="post-create"),
    path('blogpost/<int:pk>/', PostDetailView.as_view(), name="blog-post"),
    path('blogpost/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blogpost/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('blogpost/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]