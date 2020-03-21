from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse
from .models import Post
from .forms import PostForm


# Create your views here.
def index(request):
    # return HttpResponse("asdsa")
    return render(request, 'index.html')


def leave_feedback(request):
    if request.method == 'POST':
        form = PostForm(request.POST)







        print(form['name'].value(), '\t<-- name')
        print(form['email'].value(), '\t<-- email')
        print(request.POST.get('message'), '\t<-- message')












        # p = Post(
        #     name=form['name'].value(), 
        #     email=form['email'].value(),
        #     message=request.POST.get('message'),
        #     )
        # p.save_base()
    return HttpResponseRedirect('../home')
