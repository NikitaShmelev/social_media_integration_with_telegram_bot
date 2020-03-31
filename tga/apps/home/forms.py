from django import forms
from .models import Feedback
from .models import UserProfile
from .models import Channel
from .models import Post
from .models import PostMedia
from .models import PostLocation

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        
        fields = (
            'name',
            'email',
            'message',
        )
        widgets = {
            'name': forms.TextInput,
            'email': forms.TextInput,
        }
    

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        
        fields = (
            'user_id',
            'username',
            'email',
            'language'
        )
        widgets = {
            'username': forms.TextInput,
            'email': forms.TextInput,
            'language': forms.TextInput,
        }


class ChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = (
            'channel_id',
        )
        

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'created_at',
            'creator_name',
            'user',
        )

class PostLocationForm(forms.ModelForm):

    class Meta:
        model = PostLocation
        fields = (
            'post',
            'latitude',
            'longitude',
        )
        

class PostMediaForm(forms.ModelForm):

    class Meta:
        model = PostMedia
        fields = (
            'post',
            'media_1',
            'media_2',
            'media_3',
            'media_4',
            'media_5',
            'media_6',
            'media_7',
            'media_8',
            'media_9',
        )