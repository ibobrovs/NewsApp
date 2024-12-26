from django_filters import FilterSet, CharFilter, ChoiceFilter, DateFilter, RangeFilter
from django import forms
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    category = CharFilter(field_name='postCategory__name', lookup_expr='icontains', label='Категория')
    dateCreation = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        label='Позже указываемой даты',
        widget=forms.DateInput(attrs={'type': 'date', })
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'dateCreation']
