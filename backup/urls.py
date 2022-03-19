from django.conf.urls import url
from django.contrib import admin
from .views import *
from . import views


admin.autodiscover()

app_name = 'backup'

urlpatterns = [

    url(r'^backup/$', views.backup, name='backup'),
    url(r'^database$', views.database_backup, name='database_backup'),
    url(r'^download-file/$', views.downloadFile, name='downloadFile'),
    url(r'^delete-backup$', views.DeleteBackup, name='delete_backup'),
    ]
