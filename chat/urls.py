from django.urls import path
from django.conf.urls import url
from .views import *

app_name='faq'

urlpatterns = [
    url(r'^Add-To-Group/$', AddUserToGroup, name='AddToGroup'),
 
]
