from django.conf.urls import url
from .views import *

app_name = 'dblogger'


urlpatterns = [
    url(r'^all-loggs/$', Loggs, name='loggs'),
    url(r'^log-view/$', LogView, name='log_view'),

    ]
