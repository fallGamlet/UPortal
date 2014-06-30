# coding: utf-8
from django.conf.urls import patterns, url, include
from UPortal import views

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^UPortal/', include('UPortal.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),

    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^blog/', include('blog.urls')),
    
    
    (r'^$', views.main),
    (r'^help/$', views.helps),
    (r'^private/$', views.private_cabinet),
    (r'^news/$', views.news),
    (r'^cathedra/$', views.cathedra_info),
    (r'^cathedra/(\d+)/$', views.cathedra_info),
    (r'^cathedra/direction/$', views.direction_info),
    (r'^cathedra/direction/(\d+)/$', views.direction_info),
    (r'^normdocument/$', views.normative_document),
    (r'^normdocument/(\d+)/$', views.normative_document),
    (r'^articles/$', views.articles),
    (r'^schedule/$', views.schedule),
    (r'^content/$', views.content),
    (r'^content/search/$', views.search),
    (r'^content/search/article/$', views.search_article),
    (r'^curdate/$', views.getcurrentdate),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
