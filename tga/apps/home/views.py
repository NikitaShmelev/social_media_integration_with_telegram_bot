from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse("asdsa")
    return render(request, 'index.html')


def leave_feedback(request):
    pass
