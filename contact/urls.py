from django.urls import path
from .views import *

app_name='contactapp'

urlpatterns = [
    path('', ContactUs.as_view(), name='contact_us'),
    path('SendMailReply/', send_reply.as_view(), name='SendReply'),
    path('contacts/', contacts, name='contacts'),
    path('View-Reply/', DisplayReply, name='view_reply'),
]
