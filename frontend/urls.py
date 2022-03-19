from django.conf.urls import url
from django.contrib import admin
from .views import *
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

app_name = 'frontend'

sitemaps = {
 'pages': StaticSitemap,
}


urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),
        url(r'^robots.txt$', robot, name='robots'),
    url(r'^robots/$',robot, name='robots'),
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
