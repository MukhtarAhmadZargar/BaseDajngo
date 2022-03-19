from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import reverse_lazy, path
from .views import *
from accounts import views
from django.contrib.auth import views as auth_views


admin.autodiscover()

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^password_reset/$', views.ResetPasswordView.as_view(success_url = reverse_lazy('accounts:password_reset_done'),
                                                                   html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    ]