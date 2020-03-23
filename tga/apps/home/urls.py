from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('leave_feedback', views.leave_feedback, name='leave_feedback'),
]
