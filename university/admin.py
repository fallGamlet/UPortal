#! /usr/bin/python
# coding: utf-8 

from django.contrib import admin
from university.models import *


class WorkerInlineAdmin(admin.TabularInline):
	model = Worker
	extra = 1

class CathedraAdmin(admin.ModelAdmin):
	inlines = (WorkerInlineAdmin,)
	fieldsets = (
        (None, {
			'classes': ['extrapretty'],
            'fields': ('sname', 'name', 'faculty', 'description')
        }),
        (u'Пост', {
			'classes': ('collapse',), 
			'fields': ('post',)
		}),
    )

class BookTypeAdmin(admin.ModelAdmin):
    list_filter = ('sname',)

class SubjectAdmin(admin.ModelAdmin):
    pass
    #list_filter = ('sname',)

class DirectionAdmin(admin.ModelAdmin):
	list_filter = ('educationtype', 'cathedra')
	formfield_overrides = {
		models.ManyToManyField: {
			'widget': admin.widgets.FilteredSelectMultiple(u'дисциплины', is_stacked=False)
		},
	}

class BookAdmin(admin.ModelAdmin):
    list_filter = ('booktype', 'subjects')
    #raw_id_fields = ('subject',)
    formfield_overrides = {
		models.ManyToManyField: {
			'widget': admin.widgets.FilteredSelectMultiple(u'дисциплины', is_stacked=False)
		},
	}

class NormativeDocumentAdmin(admin.ModelAdmin):
    list_filter = ('doctype',)

class BellScheduleAdmin(admin.ModelAdmin):
    list_filter = ('num',)

admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Cathedra, CathedraAdmin)
admin.site.register(EducatingType)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(BookType, BookTypeAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Worker)
admin.site.register(WorkerType)
admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(Article)
admin.site.register(News)
admin.site.register(BellSchedule, BellScheduleAdmin)
admin.site.register(NormativeDocumentType)
admin.site.register(NormativeDocument, NormativeDocumentAdmin)
admin.site.register(NumeratorWeek)
admin.site.register(WelcomeMessage)

