#! /usr/bin/python
# coding: utf-8 

from django.contrib import admin
from blog.models import *


class TagsAdmin(admin.ModelAdmin):
    pass


class ArticlePermissionAdmin(admin.ModelAdmin):
    pass


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    inlines = (CommentInlineAdmin,)
    list_filter = ('author',)
    formfield_overrides = {
        models.ManyToManyField: {
            'widget': admin.widgets.FilteredSelectMultiple(u'теги', is_stacked=False)
        },
    }


admin.site.register(Tags, TagsAdmin)
admin.site.register(ArticlePermission, ArticlePermissionAdmin)
admin.site.register(Article, ArticleAdmin)


