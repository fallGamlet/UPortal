#! /usr/bin/python
# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from form import LoginForm

def main(request):
    """
    :param request:
    :return:
    """
    user = request.user
    if user.is_anonymous():
        return HttpResponseRedirect("/blog/login/")
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

    pass