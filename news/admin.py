from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'dateCreation', 'author', 'categoryType', 'rating')
    list_filter = ('categoryType', 'dateCreation')
    search_fields = ('title', 'categoryType')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Показываем только поле name, так как других полей у Category нет.


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough')  # Показываем связи постов с категориями.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentPost', 'commentUser', 'text', 'dateCreation', 'rating')
    list_filter = ('dateCreation', 'rating')
