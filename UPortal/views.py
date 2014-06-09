#! /usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
import sys
import datetime
import copy
from university import models
from university import forms

urlvoc = {
	"": u"Главная",
	"news": u"Новости",
	"help": u"Помощь",
	"search": u"Поиск",
	"articles": u"Статьи",
	"content": u"Учебный материал",
	"cathedra": u"Информация о кафедрах",
	"direction": u"Направления",
	"normdocument": u"Нормативные документы",
	"schedule": u"Расписание"
	}

menulinks = (
	("/", u"Главная"),
	("/cathedra", u"Информация о кафедрах"),
	("/cathedra/direction/", u"Информация о направлениях"),
	("/news/", u"Новости и объявления"),
	("/schedule/", u"Расписание"),
	("/normdocument", u"Нормативные документы"),
	("/content/", u"Учебный материал (поиск)"),
	#("/search/", u"Поиск"),
	)


def main(response):
	params = dict()
	params['menulinks'] = menulinks
	params['links'] = getlinks(response)
	params['welcomemessage'] = getLastWelcomeMessage()
	params['news'] = getNews(5)
	params['bellschedule'] = models.BellSchedule.objects.order_by('num')
	params['numeratorweek'] = getLastNumeratorWeek()
	#
	return render_to_response('main.djhtml', params)
	
def helps(response):
	links = getlinks(response)
	return render_to_response('help.djhtml', {'menulinks': menulinks, 'links': links})
	
def search(response):
	links = getlinks(response)
	if response.method == 'GET':
		sform = forms.SearchBook(response.GET)
		if sform.is_valid() and not sform.is_empty():
			cd = sform.cleaned_data
			books = []
			qtitle = Q(title__icontains = cd['title'])
			qauthor = Q()
			if cd['authors']:
				authors = cd['authors'].split(' ')
				for author in authors:
					qauthor |= Q(authors__icontains = author)
			if cd['btype']:
				qbtype = Q(booktype__pk__in = cd['btype'])
			else:
				qbtype = Q()
			if cd['subjects']:
				qsubject = Q(subjects__pk__in = cd['subjects'])
			else:
				qsubject = Q()
			books += models.Book.objects.filter(qtitle, qauthor, qbtype, qsubject).distinct()
			return render_to_response('search.djhtml', {'menulinks': menulinks, 'links': links, 'sform': sform, 'books': books})
	else:
		sform = forms.SearchBook()
	
	return render_to_response('search.djhtml', {'menulinks': menulinks, 'links': links, 'sform': sform})

def content(response):
	links = getlinks(response)
	return render_to_response('content.djhtml', {'menulinks': menulinks, 'links': links})

def private_cabinet(response):
	links = getlinks(response)
	return render_to_response('private.djhtml', {'menulinks': menulinks, 'links': links})
	
def news(response):
	links = getlinks(response)
	newslist = []
	today =  datetime.date.today()
	newslist = models.News.objects.filter(enddate__gt = today).order_by('-startdate', '-weight')
	return render_to_response('news.djhtml', {'menulinks': menulinks, 'links': links, 'news': newslist})
	
def articles(response):
	links = getlinks(response)
	articles = models.Article.objects.all()
	return render_to_response('articles.djhtml', {'menulinks': menulinks, 'links': links, 'articles': articles})
	
def schedule(response):
	links = getlinks(response)
	return render_to_response('schedule.djhtml', {'menulinks': menulinks, 'links': links})
	
def cathedra_info(response, cath_pk=None):
	links = getlinks(response)
	if cath_pk:
		departments = models.Cathedra.objects.filter(pk = cath_pk)
		if departments:
			links[-1] = [links[-1][0], departments[0].sname]
		else:
			links.pop()
	else:
		departments = models.Cathedra.objects.order_by('name')
	
	educationtypes = list(models.EducatingType.objects.order_by('name'))
	directions = list(models.Direction.objects.order_by('name'))
	
	for dep in departments:
		dep.edtypes = copy.deepcopy(educationtypes)
		for edtype in dep.edtypes:
			edtype.directions = list()
			for direction in directions:
				if direction.cathedra.pk == dep.pk and direction.educationtype.pk == edtype.pk:
					edtype.directions.append(direction)
			
	return render_to_response('cathedra_info.djhtml', {'menulinks': menulinks, 'links': links, 'departments':departments})

def direction_info(response, dir_pk=None):
	links = getlinks(response)
	if dir_pk:
		directions = models.Direction.objects.filter(pk = dir_pk)
		if directions: links[-1] = [links[-1][0], directions[0].sname]
		else: links.pop()
		edtypes = None
	else:
		edtypes = models.EducatingType.objects.all()
		directions = models.Direction.objects.order_by('educationtype', 'name')
	return render_to_response('direction_info.djhtml', {'menulinks': menulinks, 'links': links, 'directions':directions, 'edtypes': edtypes})

def normative_document(response, dir_pk=None):
	links = getlinks(response)
	if dir_pk:
		directions = models.Direction.objects.filter(pk = dir_pk)
		normdocs = models.NormativeDocument.objects.filter(direction = dir_pk).order_by('doctype')
		if directions: 
			links[-1] = [links[-1][0], directions[0].sname]
		else: 
			links.pop()
		edtypes = None
	else:
		directions = models.Direction.objects.order_by('educationtype', 'name')
		normdocs = models.NormativeDocument.objects.all()
		edtypes = models.EducatingType.objects.all()
	
	doctypes = models.NormativeDocumentType.objects.order_by('name')
	for direct in directions:
		direct.doctypes = dict([(t.pk, [t.pk, t.name]) for t in doctypes])
		for ndoc in normdocs:
			if ndoc.direction.pk == direct.pk:
				direct.doctypes[ndoc.doctype.pk].append(ndoc)
		direct.doctypes = direct.doctypes.values()
	return render_to_response('normative_document.djhtml', {'menulinks': menulinks, 'links': links, 'directions':directions, 'edtypes': edtypes})


def getNews(count=None):
	today =  datetime.date.today()
	news = models.News.objects.filter(enddate__gt = today).order_by('-startdate')
	if count:
		news = news[:5]
	#
	return news

def getLastWelcomeMessage():
	welcmess = models.WelcomeMessage.objects.order_by('-date')[:1]
	if len(welcmess) > 0:
		welcmess = welcmess[0]
	else:
		welcmess = None
	#
	return welcmess

def getLastNumeratorWeek():
	numeratorweek = models.NumeratorWeek.objects.order_by('-date')[:1]
	if len(numeratorweek) > 0:
		numeratorweek = numeratorweek[0]
	else:
		numeratorweek = None
	#
	return numeratorweek

def getlinks(response):
	href = response.path
	links = href.split("/")
	links.pop()
	links[0] = ["/", urlvoc[links[0]]]
	for i in range(1, len(links)):
		if links[i] in urlvoc:
			links[i] = [links[i-1][0] + links[i]+"/", urlvoc[links[i]]]
		else:
			links[i] = [links[i-1][0] + links[i]+"/", links[i]]
	#
	return links

def getcurrentdate(response):
	curdate = datetime.date.today()
	print "method in, date: "+str(curdate)
	import json
	print "imported json lib"
	res = json.dumps({"curdate": str(curdate)})
	print res
	print "method out"
	#
	return HttpResponse(res)
