from django import forms
from .models import Feedback
from .models import UserProfile

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
            'name': forms.TextInput,
            'email': forms.TextInput,
            'language': forms.TextInput,
        }