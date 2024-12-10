
from django.views.generic import ListView, DetailView
from .models import Post, PostCategory, Author, Category, Comment


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    pk_url_kwarg = 'id'