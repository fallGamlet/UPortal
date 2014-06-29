# coding: utf-8
from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'^user/$', 'blog.views.main'),
    url(r'^login/', 'blog.views.log_in'),
    url(r'^logout/', 'blog.views.log_out'),
    url(r'^article/', 'blog.views.article_list'),
)
