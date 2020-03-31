from django.contrib import admin

from .forms import FeedbackForm
from .models import Feedback

from .forms import UserProfileForm
from .models import UserProfile

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    form = FeedbackForm


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'language')
    form = UserProfileForm
