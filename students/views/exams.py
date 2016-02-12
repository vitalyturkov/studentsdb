# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.exams import Exam


def exams_list(request):
	exams = Exam.objects.all()
	order_by = request.GET.get('order_by', 'tittle')
	if order_by in ('tittle', 'examtime', 'teach', 'exam_group'):
		exams = exams.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			exams = exams.reverse()




	n = 3	
	paginator = Paginator(exams, n)
	page = request.GET.get('page', '1')
	try:
		exams = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		exams = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		exams = paginator.page(paginator.num_pages)


	numbs=[]
	for i in range(n):
		numbs.append((int(page)-1)*n+i+1)




	return render(request, 'students/exams_list.html', {'exams': exams, 'numbs':numbs})


def exams_add(request):
	return HttpResponse('<h1>Exam Add Form<h1>')

def exams_edit(request, eid):
	return HttpResponse('<h1>Edit Exam %s</h1>' % eid)

def exams_delete(request, eid):
	return HttpResponse('<h1>Delete Exam %s</h1>' % eid)