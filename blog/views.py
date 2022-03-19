from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from comments.models import Comment, Reply
from .models import *
from rating.models import Rating
import os
import logging


db_logger = logging.getLogger('db')


'''
Blog List
'''
@login_required
def BlogList(request):
    try:
        blogs=Blog.objects.all().order_by("-id")
        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 3)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        return render(request, 'blog/blog-home.html', {"blogs":blogs} )
    except Exception as e:
        db_logger.exception(e)

'''
Add New Blog
'''
@login_required
def AddBlog(request):
    try:
        categories=Category.objects.all().order_by("-id")
        if len(categories)<1:
            messages.error(request,' please Add category first, then got to Add Blog!!!')
            return redirect('blog:add_catagory')
            
        if request.method=='POST':
            title=request.POST.get('title')
            body=request.POST.get('body')
            pic=request.FILES.get('blog_pic')
            ext = os.path.splitext(pic.name)[1]
            valid_extensions = ['.tif', '.tiff', '.bmp', '.jpg', '.JPG','.jpeg', '.JPEG','.gif','.png','.PNG']
            if not ext.lower() in valid_extensions:
                messages.error(request, 'Unsupported FIle Format.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            category=request.POST.get('cate')
            blog=Blog.objects.create(title=title,body=body,image_file=pic,
                        category= Category.objects.get(id=category),created_by_id=User.objects.get(id=request.user.id))
            blog.save()
            messages.success(request,'Blog Added Successfully!!!')
            return redirect('blog:blog_list')
        return render(request, 'blog/add-blog.html',{'categories':categories})
    except Exception as e:
        db_logger.exception(e)

'''
View Blog 
'''
@login_required
def BlogDetail(request,id):
    try:
        blog=Blog.objects.get(id=id)
        return render(request, 'blog/view-blog.html',{'blog':blog})
    except Exception as e:
        db_logger.exception(e)
'''
Delete Blog 
'''
@login_required
def DeleteBlog(request):
    try:
        id=request.GET.get('id')
        blog=Blog.objects.get(id=id)
        if blog:
            blog.delete()
        messages.success(request, 'Blog Deleted Successfully')
        return redirect('blog:blog_list')
    except Exception as e:
        db_logger.exception(e)

'''
Edit Blog 
'''
class EditBlog(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        try:
            blog=Blog.objects.get(id=request.GET.get("id"))
            categories = Category.objects.all().order_by('-id')
            return render(request, 'blog/edit-blog.html',{"blog":blog,'categories':categories})
        except Exception as e:
            db_logger.exception(e)
    
    def post(self,request,*args,**kwargs):
        try:
            id=request.GET.get("id")
            blog=Blog.objects.get(id=request.GET.get("id"))

            if request.POST.get("title"):
                blog.title=request.POST.get("title")
                
            if request.POST.get("cate"):
                blog.category =  Category.objects.get(id=request.POST.get("cate"))
                
            if request.POST.get("body"):
                blog.body = request.POST.get("body")
        
            if request.FILES.get("blog_pic"):
                blog.image_file= request.FILES.get("blog_pic")
                
            blog.save()
            messages.success(request, 'Blog Edited Successfully')

            return redirect('blog:blog_detail' , id=blog.id)
        except Exception as e:
            db_logger.exception(e)

'''
Category Listing
'''
@login_required
def TotalCategory(request):
    try:
        category = Category.objects.all().order_by('id')
        return render(request, 'blog/category.html',{'category':category})
    except Exception as e:
        db_logger.exception(e)

'''
CRUD on Category
'''
@login_required
def AddCategory(request):
    try:
        if request.method=='POST':
            title=request.POST.get('title')
            if request.POST.get('desc'):
                desc=request.POST.get('desc')
            else:
                desc="Does Not Exist"
            Category.objects.create(title=title, description=desc,created_by_id=User.objects.get(id=request.user.id))
            messages.success(request,'Catagory Added Successfully!!!')
            return redirect('blog:Catagory')  
        return render(request, 'blog/add-category.html')   
    except Exception as e:
        db_logger.exception(e)

@login_required
def EditCategory(request):
    try:
        id=request.GET.get('id')
        category= Category.objects.get(id=id)
        if request.method=='POST':
            if request.POST.get('title'):
                category.title=request.POST.get('title')
            if request.POST.get('desc'):
                category.description=request.POST.get('desc')
            category.save()
            messages.success(request,'Catagory Edited Successfully!!!')
            return redirect('blog:Catagory') 
            
        return render(request, 'blog/edit-category.html',{'category':category})
    except Exception as e:
        db_logger.exception(e)


@login_required
def DeleteCategory(request):
    try:

        id=request.GET.get('id')
        category=Category.objects.get(id=id)
        if category:
            category.delete()
            messages.success(request, 'Category Deleted Successfully')
        return redirect('blog:Catagory')
    except Exception as e:
        db_logger.exception(e)

'''
Blog for All Users
'''

def BlogListing(request):
    try:
        blogs = Blog.objects.all().order_by('-id')
        blogs=Blog.objects.all().order_by("-id")
        page = request.GET.get('page', 1)
        paginator = Paginator(blogs, 6)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        return render(request, 'blog/blog-listing.html',{'status':'blog', 'blogs':blogs })
    except Exception as e:
        db_logger.exception(e)

def Blog4User(request,id):
    try:   
        blog=Blog.objects.get(id=id)
        blog.views= blog.views +1
        blog.save()
        total_rating = Rating.objects.filter(blog= Blog.objects.get(id=blog.id)).count()
        total_stars = Rating.objects.filter(blog= Blog.objects.get(id=blog.id))
        total=0
        for stars in total_stars:
            total+=stars.rating
        avg_rating=total/total_rating
        try:
            comments = Comment.objects.filter(post=blog.id).order_by('-id')
        except:
            comments = None

        try:
            replies=Reply.objects.all().order_by('-id')
        except:
            replies=None
        try:
            ratings=Rating.objects.filter(blog= Blog.objects.get(id=blog.id),user=User.objects.get(id=request.user.id))
        except:
            ratings=None
    
        return render(request, 'blog/blog-detail.html', {'blog':blog, 'comments':comments,'replies':replies ,'avg_rating':avg_rating, 'ratings': ratings}) 
    except Exception as e:
        db_logger.exception(e)


