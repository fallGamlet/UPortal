#! /usr/bin/python
# coding: utf-8

from django.db import models
from django.contrib import admin
from django.contrib.auth import User
from ckeditor.fields import RichTextField
import datetime

class ArticlePermission(models.Model):
	name = models.CharField(max_length = 50, verbose_name = 'название')
	def __unicode__(self):
		return u'%s' %name
	class Meta:
		verbose_name = 'уровень доступа'
		verbose_name_plural = 'уровни доступа'


class Article(models.Model):
	author = models.ForeignKey(User, verbose_name = 'Автор')
	permision = models.ForeignKey(ArticlePermission, verbose_name = 'Уровень доступа')
	title = models.CharField(max_length = 120, verbose_name = 'Заголовок')
	body = RichTextField(verbose_name = 'Седержание', config_name='default')
	date = models.DateField(auto_now = True, verbose_name = 'Дата', default = datetime.datetime.now())
	def __unicode__(self):
		return u'%s %s' %(self.author, self.title)
	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
