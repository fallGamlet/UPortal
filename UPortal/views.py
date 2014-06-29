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
    ("/content/", u"Учебный материал (поиск)"),  # ("/search/", u"Поиск"),
)


def main(request):
    params = dict()
    params['menulinks'] = menulinks
    params['links'] = getlinks(request)
    params['welcomemessage'] = getLastWelcomeMessage()
    params['news'] = getNews(5)
    params['bellschedule'] = models.BellSchedule.objects.order_by('num')
    params['numeratorweek'] = getLastNumeratorWeek()
    params['user'] = request.user
    #
    return render_to_response('main.html', params)


def helps(request):
    links = getlinks(request)
    return render_to_response('help.html', {'menulinks': menulinks, 'links': links, 'user':request.user})


def search(request):
    links = getlinks(request)
    if request.method == 'GET':
        sform = forms.SearchBook(request.GET)
        if sform.is_valid() and not sform.is_empty():
            cd = sform.cleaned_data
            books = []
            qtitle = Q(title__icontains=cd['title'])
            qauthor = Q()
            if cd['authors']:
                authors = cd['authors'].split(' ')
                for author in authors:
                    qauthor |= Q(authors__icontains=author)
            if cd['btype']:
                qbtype = Q(booktype__pk__in=cd['btype'])
            else:
                qbtype = Q()
            if cd['subjects']:
                qsubject = Q(subjects__pk__in=cd['subjects'])
            else:
                qsubject = Q()
            books += models.Book.objects.filter(qtitle, qauthor, qbtype, qsubject).distinct()
            return render_to_response('search.html',
                                      {'menulinks': menulinks, 'links': links, 'sform': sform,
                                       'books': books, 'user':request.user})
    else:
        sform = forms.SearchBook()

    return render_to_response('search.html', {'menulinks': menulinks, 'links': links, 'sform': sform, 'user':request.user})


def content(request):
    links = getlinks(request)
    return render_to_response('content.html', {'menulinks': menulinks, 'links': links, 'user':request.user})


def private_cabinet(request):
    links = getlinks(request)
    return render_to_response('private.html', {'menulinks': menulinks, 'links': links, 'user':request.user})


def news(request):
    links = getlinks(request)
    newslist = []
    today = datetime.date.today()
    newslist = models.News.objects.filter(enddate__gt=today).order_by('-startdate', '-weight')
    return render_to_response('news.html',
                              {'menulinks': menulinks, 'links': links, 'news': newslist, 'user':request.user})


def articles(request):
    links = getlinks(request)
    articles = models.Article.objects.all()
    return render_to_response('articles.html',
                              {'menulinks': menulinks, 'links': links, 'articles': articles, 'user':request.user})


def schedule(request):
    links = getlinks(request)
    return render_to_response('schedule.html', {'menulinks': menulinks, 'links': links, 'user':request.user})


def cathedra_info(request, cath_pk=None):
    links = getlinks(request)
    if cath_pk:
        departments = models.Cathedra.objects.filter(pk=cath_pk)
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

    return render_to_response('cathedra_info.html',
                              {'menulinks': menulinks, 'links': links, 'departments': departments, 'user':request.user})


def direction_info(request, dir_pk=None):
    links = getlinks(request)
    if dir_pk:
        directions = models.Direction.objects.filter(pk=dir_pk)
        if directions:
            links[-1] = [links[-1][0], directions[0].sname]
        else:
            links.pop()
        edtypes = None
    else:
        edtypes = models.EducatingType.objects.all()
        directions = models.Direction.objects.order_by('educationtype', 'name')
    return render_to_response('direction_info.html',
                              {'menulinks': menulinks, 'links': links, 'directions': directions,
                               'edtypes': edtypes, 'user':request.user})


def normative_document(request, dir_pk=None):
    links = getlinks(request)
    if dir_pk:
        directions = models.Direction.objects.filter(pk=dir_pk)
        normdocs = models.NormativeDocument.objects.filter(direction=dir_pk).order_by('doctype')
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
    return render_to_response('normative_document.html',
                              {'menulinks': menulinks, 'links': links, 'directions': directions,
                               'edtypes': edtypes, 'user':request.user})


def getNews(count=None):
    today = datetime.date.today()
    news = models.News.objects.filter(enddate__gt=today).order_by('-startdate')
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


def getlinks(request):
    href = request.path
    links = href.split("/")
    links.pop()
    links[0] = ["/", urlvoc[links[0]]]
    for i in range(1, len(links)):
        if links[i] in urlvoc:
            links[i] = [links[i - 1][0] + links[i] + "/", urlvoc[links[i]]]
        else:
            links[i] = [links[i - 1][0] + links[i] + "/", links[i]]
    #
    return links


def getcurrentdate(request):
    curdate = datetime.date.today()
    print "method in, date: " + str(curdate)
    import json

    print "imported json lib"
    res = json.dumps({"curdate": str(curdate)})
    print res
    print "method out"
    #
    return HttpResponse(res)
