from django.contrib import admin
from .models import Post, Author, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'dateCreation', 'author', 'categoryType', 'rating')
    list_filter = ('categoryType', 'dateCreation')
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
