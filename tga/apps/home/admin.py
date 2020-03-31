from django.contrib import admin

from .forms import FeedbackForm
from .models import Feedback

from .forms import UserProfileForm
from .models import UserProfile

from .forms import ChannelForm
from .models import Channel

from .forms import PostForm
from .models import Post

from .forms import PostMediaForm
from .models import PostMedia

from .forms import PostLocationForm
from .models import PostLocation

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    form = FeedbackForm


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'language')
    form = UserProfileForm


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'channel_id')
    form = ChannelForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'creator_name', 'created_at')
    form = PostForm


@admin.register(PostMedia)
class PostMediaAdmin(admin.ModelAdmin):
    list_display = (
        'post', 
        'media_1', 'media_2', 'media_3', 
        'media_4', 'media_5', 'media_6', 
        'media_7', 'media_8', 'media_9', 
        )
    form = PostMediaForm


@admin.register(PostLocation)
class PostLocationAdmin(admin.ModelAdmin):
    list_display = ('post', 'latitude', 'longitude',)
    form = PostLocationForm