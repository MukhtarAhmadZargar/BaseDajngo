from django.urls import path
from django.conf.urls import url, include
from .views import *

app_name='blog'

urlpatterns = [
    url(r'^BlogListing/$', BlogListing, name='BlogsListing'),
    path('Blogs/<int:id>', Blog4User, name='Blogs4User'),

    url(r'^Blog-List/$', BlogList, name='blog_list'),
    url(r'^Add-Blog/$', AddBlog, name='add_blog'),
    path('Blog-Detail/<int:id>',BlogDetail, name='blog_detail'),
    url(r'^Edit-Blog/$', EditBlog.as_view(), name='edit_blog'),
    url(r'^Delete-Blog/$', DeleteBlog, name='delete_blog'),

    url(r'^catagory/$', TotalCategory, name='Catagory'),
    url(r'^Add-catagory/$', AddCategory, name='add_catagory'),
    url(r'^Edit-catagory/$', EditCategory, name='edit_category'),
    url(r'^delete-catagory/$', DeleteCategory, name='delete_category'),

    
   
]
