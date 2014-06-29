#! /usr/bin/python
# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label=u'Логин')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput())
