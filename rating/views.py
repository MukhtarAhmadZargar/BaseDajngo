
from django.contrib import messages
from django.shortcuts import render
from .models import Rating
from blog.models import Blog
from accounts.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def Ratings(request):
    blog_id=request.GET.get('id')
    if request.method=="POST":
        rating=request.POST.get('rate')
        print(rating)
        Rating.objects.create(rating=rating,blog=Blog.objects.get(id=blog_id),user=User.objects.get(id=request.user.id))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

