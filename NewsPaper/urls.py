from django.contrib import admin
from django.urls import path, include
from news.views import Post, PostDetail, NewsCreate, ArticleCreate, PostUpdate, PostDelete
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('admin/', admin.site.urls),
   path('news/', include('news.urls')),
   path("accounts/", include("allauth.urls")),
   path('', include('board.urls')),
   path('', Post),
   path('<int:pk>/', cache_page(60 * 10)
   (PostDelete.as_view()), name='post_detail'),
   path('create/', NewsCreate.as_view(), name='post_create'),
   path('create/', ArticleCreate.as_view(), name='post_create'),
   path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]
