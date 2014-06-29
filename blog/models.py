#! /usr/bin/python
# coding: utf-8

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime


class Tags(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class ArticlePermission(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')

    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta:
        verbose_name = 'уровень доступа'
        verbose_name_plural = 'уровни доступа'


class Article(models.Model):
    author = models.ForeignKey(User, verbose_name='автор')
    read_access = models.ForeignKey(ArticlePermission, verbose_name='уровень доступа')
    title = models.CharField(max_length=120, verbose_name='заголовок')
    body = RichTextField(verbose_name='седержание', config_name='default')
    date = models.DateField(auto_now=True, verbose_name='дата', default=datetime.datetime.now())
    tags = models.ManyToManyField(to=Tags, verbose_name='теги')

    def __unicode__(self):
        return u'%s %s' % (self.author, self.title)

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Comment(models.Model):
    author = models.ForeignKey(User, verbose_name='автор')
    article = models.ForeignKey(Article, verbose_name='статья')
    body = models.TextField(max_length=1000, verbose_name='текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __unicode__(self):
        return u'%s %s' % (self.article, self.author,)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'коментарии'


class Likes(models.Model):
    author = models.ForeignKey(User, verbose_name='автор')
    article = models.ForeignKey(Article, verbose_name='статья')
    islike = models.BooleanField(default=False, verbose_name='понравилось')
    isunlike = models.BooleanField(default=False, verbose_name='не понравилось')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __unicode__(self):
        return u'%s %s. Like:%s, Unlike:%s' % (self.article, self.author, self.islike, self.isunlike,)

    class Meta:
        verbose_name = 'одобрение'
        verbose_name_plural = 'одобрения'


# class Book(models.Model):
#     owner = models.ForeignKey(User, verbose_name='владелец')
#     read_access = models.ForeignKey(ArticlePermission, verbose_name='уровень доступа')
#     author = models.CharField(max_length=256, verbose_name='заголовок')
#     title = models.CharField(max_length=256, verbose_name='заголовок')
#     description = models.TextField(max_length=512, verbose_name='описание',)
#     bookfile = models.FileField(upload_to='', )
#     date = models.DateField(auto_now=True, verbose_name='дата', default=datetime.datetime.now())
#     tags = models.ManyToManyField(to=Tags, verbose_name='теги')
#
#     def __unicode__(self):
#         return u'%s %s' % (self.author, self.title)
#
#     class Meta:
#         verbose_name = 'книга'
#         verbose_name_plural = 'книги'