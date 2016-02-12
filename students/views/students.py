# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.students import Student



def students_list(request):
	students = Student.objects.all()
	# try to order students list
	order_by = request.GET.get('order_by', 'last_name')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()

	n = 3
	paginator = Paginator(students, n)
	page = request.GET.get('page', '1')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		students = paginator.page(paginator.num_pages)


	numbs=[]
	for i in range(n):
		numbs.append((int(page)-1)*n+i+1)


	
	"""
	
	pag = request.GET.get('page', '1')
	if pag == '1':
		students_sort = students_sort.all()[0:5]

	if pag == '2':
		students_sort = students_sort.all()[5:10]
	"""

	return render(request, 'students/students_list.html',
	{'students': students, 'current_page': page, 'numbs': numbs})



def students_add(request):
	return HttpResponse('<h1>Student Add Form<h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)