from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        
        fields = (
            'name',
            'email',
            'message',
        )
        widgets = {
            'name': forms.TextInput,
            'email': forms.TextInput,
        }
    