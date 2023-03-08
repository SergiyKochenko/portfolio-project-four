from .models import Comment
from django import forms
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'content', 'featured_image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

