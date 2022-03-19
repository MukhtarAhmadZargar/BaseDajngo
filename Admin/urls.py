from django.conf.urls import url, include
from django.contrib import admin
from django.urls import reverse_lazy, path
from .views import *

admin.autodiscover()

app_name = 'Admin'

urlpatterns = [
    url(r'^deleteuser/$', DeleteUser, name='delete_user'),
    url(r'^delete-user/$', DeleteUserindex, name='Delete_User_index'),
    url(r'^users/$', Allusers, name='allusers'),
    path('view/<int:id>',ViewUser, name='View_User'),
    url(r'^add-user/$', AddUser.as_view(), name='Add_User'),
    url(r'^edit-user/$', EditUser.as_view(), name='Edit_User'),
    url(r'^change-password/$', PasswordChange.as_view(), name='Password_Change'),
    url(r'^admin/change-status-active$', ChangeStatusActive, name='change_status_active'),
    url(r'^admin/change-status-inactive$', ChangeStatusInactive, name='change_status_inactive'),
    url(r'^admin/change-status-delete$', ChangeStatusDelete, name='change_status_delete'),
    url(r'^admin/download-CSV$', Download_CSV, name='download_CSV'),
    url(r'^admin/Upload-CSV$', UploadCSV, name='Upload_CSV'),
    ]
