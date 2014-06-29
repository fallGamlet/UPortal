# coding: utf-8
from django.conf.urls import patterns, url, include
from django.conf import settings

urlpatterns = patterns('',
    url(r'^user/$', 'blog.views.main'),
    url(r'^login/$', 'blog.views.log_in'),
    url(r'^logout/$', 'blog.views.log_out'),
    url(r'^user/article/$', 'blog.views.article_list'),
    url(r'^user/article/new/$', 'blog.views.article_new'),
    url(r'^user/article/edit/(\d+)/$', 'blog.views.article_edit'),
    url(r'^user/article/remove/(\d+)/$', 'blog.views.article_remove'),
    url(r'^user/article/search', 'blog.views.search')
)
