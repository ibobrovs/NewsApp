from django.urls import path
from .views import PostList, PostDetail

urlpatterns = [
   path('', PostList.as_view(), name='news_list'),
   path('<int:id>', PostDetail.as_view(), name='news_detail'),
]