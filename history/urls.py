
from django.conf.urls import url


from django.urls import  path
from .views import *

app_name = 'history'

urlpatterns = [
    url(r'^Login-History/$', LoginHistoryView, name='login_history'),
    url(r'^Delete-History/$', DeleteHistory, name='deletehistory'),
    ]
