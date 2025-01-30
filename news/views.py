from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostFilter
from .forms import PostForm

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, Category

from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views import View
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.utils.translation import gettext as _
from .models import Category, MyModel
from django.utils import timezone
from django.shortcuts import redirect
from datetime import datetime
from datetime import datetime
import pytz


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["id"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["id"]}', obj)
        return obj


class NewsCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True

    def form_valid(self, form):
        news = form.save(commit=False)
        news.categoryType = 'NEWS'
        return super().form_valid(form)


class ArticleCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    raise_exception = True

    def form_valid(self, form):
        article = form.save(commit=False)
        article.categoryType = 'ARTICLE'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    pk_url_kwarg = 'id'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    pk_url_kwarg = 'id'


class FilteredListViewMixin:
    filter_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filter_class:
            self.filterset = self.filter_class(self.request.GET, queryset)
            return self.filterset.qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = getattr(self, 'filterset', None)
        return context


class PostList(FilteredListViewMixin, ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    filter_class = PostFilter


class PostSearch(FilteredListViewMixin, ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'search_results'
    paginate_by = 10
    filter_class = PostFilter


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


class Index(View):
    def get(self, request):
        # .  Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')

@cache_page(60 * 15)
def my_view(request):
    ...
