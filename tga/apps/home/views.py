from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post
from .forms import PostForm
import sqlite3

DATABASE_PATH = './tga/apps/ugc/management/commands/bot_dir/database.sqlite3' # development
# DATABASE_PATH = './social_media_integration_wtih_telegram_bot/tga/apps/ugc/management/commands/bot_dir/database.sqlite3' # deploy


def index(request):
    return render(request, 'index.html')


def leave_feedback(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        cur.execute('SELECT email FROM users')
        emails = tuple(i[0] for i in cur.fetchall())
        if form['email'].value().lower() in emails:
            p = Post(
                name=form['name'].value(),
                email=form['email'].value(),
                message=request.POST.get('message'),
            )
            p.save_base()
            messages.success(request, 'Thanks for your feedback!!!')
            
        else:
            messages.warning(
                request, 'Write correct email or register in the Bot before leaving feedback.')
                      
        cur.close()
        conn.close()

    return HttpResponseRedirect('../home/#contact')
