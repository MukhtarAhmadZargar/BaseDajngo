from django.contrib import admin
from django.urls import path,include
from django.conf.urls import include, url
from django.conf import settings
from accounts.views import  AdminLoginView
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/login/', AdminLoginView.as_view()),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('contact/', include('contact.urls')),
    path('accounts/', include('accounts.urls', 'accounts')),
    url('^accounts/', include('django.contrib.auth.urls')),
    path('backup/', include('backup.urls') , name="Back_up"),
    path('Admin/', include('Admin.urls') , name="Admin"),
    path('History/', include('history.urls') , name="history"),
    path('blog/', include('blog.urls') , name="blog"),
    path('comments/', include('comments.urls') , name="comments"),
    path('faq/', include('faq.urls') , name="faq"),
    path('rating/', include('rating.urls') , name="rating"),
    path('dblogger/', include('dblogger.urls') , name="dblogger"),
] 


if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, 
document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, 
document_root=settings.MEDIA_ROOT)


handler404 = 'frontend.views.error_404'
handler404 = 'frontend.views.error_404'
handler403 = 'frontend.views.error_404'