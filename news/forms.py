from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20, widget=forms.Textarea)

    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'categoryType',
            'text',
            'postCategory',
        ]
        widgets = {
            'postCategory': forms.CheckboxSelectMultiple,
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title and text and title.lower() == text.lower():
            raise ValidationError(
                "Текст не должен быть идентичен заголовку."
            )

        return cleaned_data
