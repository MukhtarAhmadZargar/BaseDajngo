
from django.conf.urls import url
from django.urls import  path
from .views import *

app_name = 'rating'

urlpatterns = [
         url(r'^rating/$', Ratings, name='rating'),

    ]
