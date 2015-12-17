# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


def journal(request):
	j_data = (
		{'id':1,
		 'first_name': u'Джек',
		 'last_name': u'Джокер'},

		{'id':2,
		 'first_name': u'Брюс',
		 'last_name': u'Уейн'},
		{'id':3,
		 'first_name': u'Кларк',
		 'last_name': u'Кент'},)

	return render(request, 'students/journal.html', {'j_data': j_data})