from django.shortcuts import render, redirect

from project.settings import LOGIN_URL
from .models import Comment, Reply
from accounts.models import User
from blog.models import Blog
from django.contrib.auth.decorators import login_required



'''
blog comments
'''
def CommentBlog(request):
    blog=Blog.objects.get(id=request.GET.get('id'))
    if request.method=='POST':
        if request.POST.get('comment'):
            comment=request.POST.get('comment')
            newcomment=Comment.objects.create(body=comment,user=User.objects.get(id=request.user.id),
            post=Blog.objects.get(id=request.GET.get('id')))
            newcomment.save()
    return redirect('blog:Blogs4User', id=blog.id)


'''
Reply To Comment
'''
@login_required
def ReplyComment(request):
    if request.method=="POST":
        blog=Blog.objects.get(id=request.POST.get('blogid'))
        reply=request.POST.get('reply')
        if reply:
            newreply=Reply.objects.create(body=reply,user=User.objects.get(id=request.user.id),
                comment=Comment.objects.get(id=request.GET.get('id')) )
            newreply.save()
    return redirect('blog:Blogs4User', id=blog.id)



