from django.contrib import admin
from .forms import PostForm
from .models import Post

@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    form = PostForm
