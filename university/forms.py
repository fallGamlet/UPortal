#! /usr/bin/python
#-*- coding: utf-8 -*-

from django import forms
import django.contrib.admin.widgets as admin_widjets
import models


class SearchBook(forms.Form):
	title = forms.CharField(label = u'Название книги', max_length = 90, required = False)
	authors = forms.CharField(label = u'Авторы', max_length = 90, required = False)
	btype = forms.ModelMultipleChoiceField(
					label = u'Типы', 
					queryset = models.BookType.objects.all(),
					#widget = admin_widjets.FilteredSelectMultiple(verbose_name=u'типы', is_stacked=False),
					required = False
				)
	subjects = forms.ModelMultipleChoiceField(
					label = u'Дисциплины', 
					queryset = models.Subject.objects.all(),
					#widget = admin_widjets.FilteredSelectMultiple(verbose_name=u'дисциплины', is_stacked=False),
					required = False
				)
	
	def is_empty(self):
		result = True
		cd = self.cleaned_data
		for key in cd:
			result &= not bool(cd[key])
		return result

