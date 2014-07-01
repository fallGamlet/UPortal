#! /usr/bin/python
# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.db.models import Q
from forms import LoginForm, ArticleFrom, SearchArticleForm
import models

def main(request):
    """
    :param request:
    :return:
    """
    perm_checked, user, muser =  check_user(request)

    user = request.user
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
    else:
        if not perm_checked:
            return HttpResponseRedirect("/")

    return render_to_response("blog_base.html", {'user': user})


def log_in(request):
    """
    :param request: request params as dictionary
    :return: rendered page
    """
    user = None
    is_empty = False
    login = None
    pwd = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
    else:
        form = LoginForm()
        is_empty = True

    if form.is_valid():
        login = form.cleaned_data['login']
        pwd = form.cleaned_data['password']
        user = auth.authenticate(username=login, password=pwd)

    if user is not None and user.is_active:
        auth.login(request, user)
        # if user.is_staff:
        #     return HttpResponseRedirect("/admin/")
        return HttpResponseRedirect("/blog/user/")

    if not is_empty and (login or pwd):
        form.errors["login_error"] = u'неверно указан логин или пароль';
    return render_to_response("blog_login.html", {'form':form}, context_instance=RequestContext(request) )


def log_out(request):
        auth.logout(request)
        return HttpResponseRedirect("/")


def article_list(request):
    perm_checked, user, muser = check_user(request)
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
    else:
        if not perm_checked:
            return HttpResponseRedirect("/")

    posts = models.Article.objects.filter(author__username=user.username)
    return render_to_response("blog_article_list.html",
                              {'articles':posts, 'user': user})


def article_new(request):
    perm_checked, user, muser = check_user(request)
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
    else:
        if not perm_checked:
            return HttpResponseRedirect("/")

    if request.method == "GET":
        form = ArticleFrom(initial={'author':muser.pk})
        return render_to_response("blog_article_edit.html",
                              {'form':form, 'user': user},
                              context_instance=RequestContext(request))
    else: # request.method == "POST"
        form = ArticleFrom(request.POST, initial={'author':muser.pk})
        if form.is_valid():
            form.save()
            return  render_to_response("blog_article_edited.html",
                                       {'message_info':'Статья успешно добавлена',
                                        'user': user})
        else:
            return render_to_response("blog_article_edit.html",
                              {'form':form, 'user': user},
                              context_instance=RequestContext(request))


def article_edit(request, article_pk=None):
    perm_checked, user, muser = check_user(request)
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
    else:
        if not perm_checked:
            return HttpResponseRedirect("/")

    if article_pk is None:
        return HttpResponseRedirect("/blog/user/article/")

    article = models.Article.objects.get(pk=article_pk, author=user)

    if request.method == "GET":
        form = ArticleFrom(instance=article)
        return render_to_response("blog_article_edit.html",
                              {'form':form, 'user': user},
                              context_instance=RequestContext(request))
    else: # request.method == "POST"
        form = ArticleFrom(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return  render_to_response("blog_article_edited.html",
                                       {'message_info':'Статья успешно изменена',
                                        'user': user})
        else:
            return render_to_response("blog_article_edit.html",
                              {'form':form, 'user': user},
                              context_instance=RequestContext(request))


def article_remove(request, article_pk=None):
    perm_checked, user, muser = check_user(request)
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
    else:
        if not perm_checked:
            return HttpResponseRedirect("/")

    if article_pk is None:
        return HttpResponseRedirect("/blog/user/article/")

    try:
        article = models.Article.objects.get(pk=article_pk, author=user)
        article.delete()
        return HttpResponseRedirect("/blog/user/article/")
    except:
        return HttpResponseRedirect("/blog/user/article/")


def check_user(request):
    user = request.user
    muser = None
    result = True
    if not user.is_authenticated():
        result &= False
    else:
        muser = auth.get_user(request)
    result &= user.has_perms(['blog.add_article', 'blog.change_article', 'blog.delete_article'])
    return (result, user, muser)


def check_access_read_artile(article=None, user=None):
    if article is None:
        return False


def search_inner(request):
    user = request.user
    form = SearchArticleForm(request.GET)
    valid, vAuth, vTitle, vTags = form.is_empty()
    #print valid, vAuth, vTitle, vTags
    if valid:
        cd = form.cleaned_data
        if vTitle:
            qtitle = Q(title__icontains=cd['title'].strip())
        else:
            qtitle = Q()

        if vAuth:
            fauthor = cd['author'].strip()
            qauthor = Q(author__username__icontains=fauthor) | \
                     Q(author__first_name__icontains=fauthor) | \
                     Q(author__last_name__icontains=fauthor)
        else:
            qauthor = Q()

        # if vTags:
        #     tagsArr = cd['tags'].split(',')
        #     newTagsArr = []
        #     for tag in tagsArr:
        #         tag = tag.strip()
        #         if len(tag)>0:
        #             newTagsArr.append(tag)
        #     print newTagsArr
        #
        #     qtag = models.Tags.objects.filter(name__icontains=tagsArr)
        #     print qtag
        #     qtags = Q(tags__name__in=qtag)
        # else:
        #     qtags = Q()
        # print qtags
        posts = models.Article.objects.filter(qauthor, qtitle)
    #
    return render_to_response("blog_article_inner_list_preview.html", {'user': user, 'articleList':posts})


def article_view_inner(request, article_pk=None):
	perm_checked, user, muser = check_user(request)
	error = None
	try:
		post = models.Article.objects.get(pk=article_pk)
	except:
		post = None
	
	if post is not None:
		if post.read_access.code == "only_logined" and not user.is_authenticated():
			post = None
			error = "Статья доступна только авторизованым пользователям!"
		else:
			if post.read_access.code == "only_mygroup" and \
				not user.is_superuser and \
				len(user.groups.filter(pk__in=post.author.groups.all())) == 0:
				post = None
				error = "Статья доступна только пользователям определенной группы!"
	return render_to_response("blog_article_inner_view.html", {'user': user, 'article':post, 'error':error})
