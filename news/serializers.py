from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    categoryType_display = serializers.CharField(source='get_categoryType_display', read_only=True)
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'categoryType', 'categoryType_display', 'dateCreation', 'postCategory', 'text', 'title', 'rating', 'preview']

    def get_preview(self, obj):
        return obj.preview()
