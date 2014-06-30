#! /usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import Article
from ckeditor import widgets as ck_widgets
#from UPortal.settings import *

class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())


class ArticleFrom(forms.ModelForm):
    class Meta:
        model = Article
        #fields = ['title', 'tags', 'read_access', 'read_access', 'body']
        #exclude = ['author',]
        widgets = {
            'author': forms.HiddenInput(),
            'tags': FilteredSelectMultiple(u'теги', is_stacked=False),
            'body': ck_widgets.CKEditorWidget(),
        }


class SearchArticleForm(forms.Form):
    author = forms.CharField(min_length=2, required=False)
    title = forms.CharField(min_length=2, required=False)
    tags = forms.CharField(min_length=2, required=False)

    def is_empty(self):
        checkAuthor = 0
        checkTitle = 0
        checkTags = 0
        self.is_valid()
        cd = self.cleaned_data
        if len(cd['author'].strip()) > 0:
            checkAuthor += 1
        if len(cd['title'].strip()) > 0:
            checkTitle += 1
        tagsArr = cd['tags'].split(',')
        for tag in tagsArr:
            if len(tag.strip()) > 0:
                checkTags += 1
        check = checkAuthor + checkTitle + checkTags
        return  (check > 0,checkAuthor>0, checkTitle>0, checkTags>0)

