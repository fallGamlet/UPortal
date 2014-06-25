#! /usr/bin/python
# coding: utf-8

from django.db import models
from django.contrib import admin
from ckeditor.fields import RichTextField
import datetime

def book_upload_path(instance, filename):
    """Generates upload path for FileField for Books"""
    res = u'books/%s/%s' % (instance.booktype.sname, filename)
    return res

def ducument_upload_path(instance, filename):
	res = u'documents/%s/%s' %(instance.doctype.pk, filename)
	return res


class MyModel():	
	def getModel(self):
		return self.__class__.__name__


class Article(models.Model, MyModel):
	author = models.CharField(max_length = 90, verbose_name = 'Автор')
	title = models.CharField(max_length = 120, verbose_name = 'Заголовок')
	body = RichTextField(verbose_name = 'Седержание', config_name='default')
	date = models.DateField(auto_now = True, verbose_name = 'Дата', default = datetime.datetime.now())
	def __unicode__(self):
		return u'%s %s' %(self.author, self.title)
	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'


class University(models.Model, MyModel):
	sname = models.CharField(max_length = 50, verbose_name = 'Сокращение')
	name = models.CharField(max_length = 200, verbose_name = 'Название')
	description = models.TextField(max_length = 1000, verbose_name ='Описание', blank=True)
	def __unicode__(self):
		return u'%s' %self.sname
	class Meta:
		verbose_name = 'Университет'
		verbose_name_plural = 'Университеты'


class Faculty(models.Model, MyModel):
	sname = models.CharField(max_length = 50, verbose_name ='Сокращение')
	name = models.CharField(max_length = 200, verbose_name ='Название')
	description = models.TextField(max_length = 1000, verbose_name ='Описание', blank = True)
	university = models.ForeignKey(University, verbose_name ='Университет')
	def __unicode__(self):
		return u'%s' %self.sname
	class Meta:
		verbose_name = 'Факультет'
		verbose_name_plural = 'Факультеты'


class Cathedra(models.Model, MyModel):
	sname = models.CharField(max_length = 50, verbose_name ='Сокращение')
	name = models.CharField(max_length = 200, verbose_name ='Название')
	description = models.TextField(max_length = 2048, verbose_name = 'Описание', blank = True)
	faculty = models.ForeignKey(Faculty, verbose_name ='Факультет')
	post = RichTextField(verbose_name = 'Пост', null=True)
	def __unicode__(self):
		return u'%s' %self.sname
	class Meta:
		verbose_name = 'Кафедра'
		verbose_name_plural = 'Кафедры'


class Subject(models.Model, MyModel):
	sname = models.CharField(max_length = 40, verbose_name ='Сокращение')
	name = models.CharField(max_length = 200, verbose_name ='Название')
	def __unicode__(self):
		return u'%s' %self.name
	class Meta:
		ordering = ['name']
		verbose_name = 'Дисциплина'
		verbose_name_plural = 'Дисциплины'


class EducatingType(models.Model, MyModel):
	name = models.CharField(max_length = 50, verbose_name ='Название')
	description = models.TextField(max_length = 1000, verbose_name = 'Описание', blank = True)
	def __unicode__(self):
		return u'%s' %self.name
	class Meta:
		ordering = ['name']
		verbose_name = 'Вид обучения'
		verbose_name_plural = 'Виды обучения'


class Direction(models.Model, MyModel):
	sname = models.CharField(max_length = 50, verbose_name ='Сокращение')
	name = models.CharField(max_length = 200, verbose_name ='Название')
	description = models.TextField(max_length = 2048, verbose_name = 'Описание', blank = True)
	cathedra = models.ForeignKey(Cathedra, verbose_name ='Кафедра')
	educationtype = models.ForeignKey(EducatingType, verbose_name='Вид обучения', null=True)
	subjects = models.ManyToManyField(Subject, verbose_name ='Дисциплины')
	post = RichTextField(verbose_name = 'Пост', null=True)
	def __unicode__(self):
		return u'%s %s' %(self.educationtype.name, self.sname)
	class Meta:
		#ordering = ['educationtype', 'cathedra', 'sname']
		verbose_name = 'Направление'
		verbose_name_plural = 'Направления'


class WorkerType(models.Model, MyModel):
	name = models.CharField(max_length = 200, verbose_name ='Название')
	def __unicode__(self):
		return u'%s' %self.name
	class Meta:
		verbose_name = 'Тип работника'
		verbose_name_plural = 'Типы работников'


class Worker(models.Model, MyModel):
	last_name = models.CharField(max_length = 60, verbose_name ='Фамилия')
	first_name = models.CharField(max_length = 60, verbose_name ='Имя')
	middle_name = models.CharField(max_length = 60, verbose_name ='Отчество')
	workertype = models.ForeignKey(WorkerType, verbose_name ='Должность')
	cathedra = models.ForeignKey(Cathedra, verbose_name = 'Кафедра')
	def __unicode__(self):
		return u'%s %s %s' %(self.last_name, self.first_name, self.middle_name)
	class Meta:
		ordering = ['last_name']
		verbose_name = 'Работник'
		verbose_name_plural = 'Работники'

	
class StudentGroup(models.Model, MyModel):
	sname = models.CharField(max_length = 40, verbose_name ='Сокращение')
	name = models.CharField(max_length = 200, verbose_name ='Название')
	direction = models.ForeignKey(Direction, verbose_name ='Направление')
	def __unicode__(self):
		return u'%s' %self.sname
	class Meta:
		verbose_name = 'Группа студентов'
		verbose_name_plural = 'Группы студентов'

	
class Student(models.Model, MyModel):
	last_name = models.CharField(max_length = 60, verbose_name ='Фамилия')
	first_name = models.CharField(max_length = 60, verbose_name ='Имя')
	middle_name = models.CharField(max_length = 60, verbose_name ='Отчество')
	studentgroup = models.ForeignKey(StudentGroup, verbose_name ='Группа')
	def __unicode__(self):
		return u'%s %s %s' %(self.first_name, self.middle_name, self.last_name)
	class Meta:
		verbose_name = 'Студент'
		verbose_name_plural = 'Студенты'


class BookType(models.Model, MyModel):
	sname = models.CharField(max_length = 60, verbose_name = 'Сокращение')
	name = models.CharField(max_length = 200, verbose_name = 'Название')
	description = models.TextField(blank = True, verbose_name = 'Описание')
	image = models.FileField(upload_to = 'preview', blank = True, verbose_name = 'Изображение', default="preview/document.png")
	def __unicode__(self):
		return u'%s' %self.name
	class Meta:
		ordering = ['name']
		verbose_name = 'Тип книги'
		verbose_name_plural = 'Типы книг'


class Book(models.Model, MyModel):
	title = models.CharField(max_length = 200, verbose_name = 'Название')
	authors = models.CharField(blank = True, max_length = 200, verbose_name = 'Авторы')
	year = models.IntegerField(null = True, blank = True, verbose_name = 'Год')
	publisher = models.CharField(max_length = 200, blank = True, verbose_name = 'Издатель')
	place = models.CharField(max_length = 60, blank = True, verbose_name = 'Место')
	page = models.IntegerField(null = True, blank = True, verbose_name = 'Страниц')
	booktype = models.ForeignKey(BookType, verbose_name = 'Тип')
	subjects = models.ManyToManyField(Subject, verbose_name = 'Дисциплины', null = True, blank = True)
	bookfile = models.FileField(max_length=512, upload_to = book_upload_path, blank = True, verbose_name = 'Файл')
	description = models.TextField(blank = True, verbose_name = 'Описание')
	def __unicode__(self):
		return u'%s' %self.title
	class Meta:
		verbose_name = 'Книга'
		verbose_name_plural = 'Книги'


class NormativeDocumentType(models.Model, MyModel):
	sname = models.CharField(max_length = 60, verbose_name = 'Сокращение')
	name = models.CharField(max_length = 200, verbose_name = 'Название')
	description = models.TextField(blank = True, verbose_name = 'Описание')
	image = models.FileField(upload_to = 'preview', blank = True, verbose_name = 'Изображение', default="preview/document.png")
	def __unicode__(self):
		return u'%s' %self.name
	class Meta:
		ordering = ['name']
		verbose_name = 'Тип нормативного документа'
		verbose_name_plural = 'Типы нормативных документов'
	

class NormativeDocument(models.Model, MyModel):
	title = models.CharField(max_length = 200, verbose_name = 'Название')
	doctype = models.ForeignKey(NormativeDocumentType, verbose_name = 'Тип')
	direction = models.ForeignKey(Direction, blank=True, null=True, verbose_name ='Направление')
	docfile = models.FileField(max_length=512, upload_to = ducument_upload_path, blank = True, verbose_name = 'Файл')
	description = models.TextField(blank = True, verbose_name = 'Описание')
	def __unicode__(self):
		return u'%s' %self.title
	class Meta:
		verbose_name = 'Нормативный документ'
		verbose_name_plural = 'Нормативные документы'


class News(models.Model, MyModel):
	title = models.CharField(max_length = 120, verbose_name = 'Заголовок')
	body = models.TextField(verbose_name = 'Седержание')
	startdate = models.DateField(verbose_name = 'Дата создания', auto_now=True, default = datetime.datetime.now())
	enddate = models.DateField(verbose_name = 'Дата актуальности', default = datetime.datetime.now())
	weight = models.IntegerField(verbose_name = 'Важность', default = 5, choices = [(i+1,i+1) for i in range(10)])
	def __unicode__(self):
		return u'%s' %(self.title)
	class Meta:
		verbose_name = 'Новость'
		verbose_name_plural = 'Новости'


class BellSchedule(models.Model, MyModel):
	num = models.IntegerField(verbose_name='Номер')
	timestart = models.TimeField(verbose_name='Начало')
	timeend = models.TimeField(verbose_name='Конец')
	def __unicode__(self):
		return u'%i: %s - %s' %(self.num, str(self.timestart), str(self.timeend))
	class Meta:
		ordering = ['num']
		verbose_name = 'Расписание звонков'
		verbose_name_plural = 'Расписания звонков'


class NumeratorWeek(models.Model, MyModel):
	date = models.DateField(verbose_name='Дата числителя')
	#date = models.DateField(verbose_name='Дата начала')
	#date = models.DateField(verbose_name='Дата окончания')
	def __unicode__(self):
		return u'%i: %s' %(self.pk, str(self.date))
	class Meta:
		ordering = ['-date']
		verbose_name = 'Расписание числителя и знаменателя'
		verbose_name_plural = 'Расписания числителя и знаменателя'


class WelcomeMessage(models.Model, MyModel):
	title = models.CharField(max_length = 100, verbose_name ='Заголовок')
	author = models.CharField(max_length = 50, verbose_name ='Автор')
	date = models.DateField(verbose_name = 'Дата', default = datetime.datetime.now())
	post = RichTextField(verbose_name = 'Пост', null=True)
	def __unicode__(self):
		return u'%s' %self.title
	class Meta:
		verbose_name = 'Приветственное сообщение'
		verbose_name_plural = 'Приветственные сообщения'




