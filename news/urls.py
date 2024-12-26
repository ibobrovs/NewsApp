from django.urls import path
from .views import (
    PostList, PostDetail, NewsCreate, ArticleCreate, PostUpdate, PostDelete, PostSearch,
)

urlpatterns = [
    path('', PostList.as_view(), name='news_list'),
    path('<int:id>', PostDetail.as_view(), name='news_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/<int:id>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('news/<int:id>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('articles/<int:id>/delete/', PostDelete.as_view(), name='article_delete'),
    path('news/<int:id>/delete/', PostDelete.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view(), name='post_search'),
]