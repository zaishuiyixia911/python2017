from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simplecmdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hostinfo/collect/$','hostinfo.views.collect'),
    url(r'^hostinfo/getjson/$','hostinfo.views.getjson'),
    url(r'^hostinfo/gettxt/$','hostinfo.views.gettxt'),
)
