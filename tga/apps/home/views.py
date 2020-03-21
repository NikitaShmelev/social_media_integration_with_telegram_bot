from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
from django.contrib import messages
from .models import Post
from .forms import PostForm
import sqlite3

DATABASE_PATH = './tga/apps/ugc/management/commands/bot_dir/database.sqlite3'

# Create your views here.
def index(request):
    # return HttpResponse("asdsa")
    return render(request, 'index.html')


def leave_feedback(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        conn = sqlite3.connect(DATABASE_PATH)
        cur = conn.cursor()
        cur.execute('SELECT email FROM users')
        emails = tuple(i[0] for i in cur.fetchall())
        messages.add_message(request, messages.INFO, 'Hello world.')
        if form['email'].value() in emails:
            p = Post(
                name=form['name'].value(),
                email=form['email'].value(),
                message=request.POST.get('message'),
            )
            p.save_base()
            # messages.add_message(
            #     request, messages.success, 'Thanks for your feedback!!!')
        else:
            pass
            # messages.add_message(
            #     request, messages.warning, 'Write correct email or register in the Bot before leaving feedback')
                                
        cur.close()
        conn.close()
            
    return HttpResponseRedirect('../home')
