from django.urls import path
from django.conf.urls import url, include
from .views import *

app_name='comments'

urlpatterns = [
    url(r'^Comment/$', CommentBlog, name='Comment_Blog'),
    url(r'^Reply/$', ReplyComment, name='Reply_Comment'),
]