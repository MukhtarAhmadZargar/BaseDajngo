from django.urls import path
from django.conf.urls import url
from .views import *

app_name='faq'

urlpatterns = [
    url(r'^Faq/$', FaqHome, name='faq_home'),
    url(r'^Add-FAQ/$', AddFAQ, name='add_blog'),
    url(r'^Edit-FAQ/$', EditFAQ.as_view(), name='Edit_FAQ'),
    url(r'^Delete-FAQ/$', DeleteFAQ, name='Delete_FAQ'),
    path('view-FAQ/<int:id>', ViewFAQ, name='View_FAQ'),
    
]
