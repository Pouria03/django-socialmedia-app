from .models import Post,Comment
from django.core.exceptions import ValidationError
from django import forms
# this form is for creating and updating posts
class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

# this class represents a form for people to comment under posts
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body' : forms.Textarea(),
        }
        labels = {
            'body' : 'comment :'
        }

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body' : forms.Textarea(),
        }
        labels = {
            'body' : 'comment :'
        }

class SearchForm(forms.Form):
    search = forms.CharField()