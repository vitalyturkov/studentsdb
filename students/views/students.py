# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def students_list(request):
   students = (
	{'id':1,
	 'first_name': u'Джек',
	 'last_name': u'Джокер',
	 'ticket': 2123,
	 'image': 'img/joker.jpg'},
	 {'id':2,
          'first_name': u'Брюс',
          'last_name': u'Уейн',
          'ticket': 254,
          'image': 'img/batman.jpg'},
	 {'id':3,
          'first_name': u'Кларк',
          'last_name': u'Кент',
          'ticket': 5332,
          'image': 'img/superman.jpg'},
) 
   return render(request, 'students/students_list.html', {'students':students})

def students_add(request):
   return HttpResponse('<h1>Student Add Form<h1>')

def students_edit(request, sid):
   return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
   return HttpResponse('<h1>Delete Student %s</h1>' % sid)