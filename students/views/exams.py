# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from ..models.exams import Exam
from ..models.groups import Group


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
	# was form posted?
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			errors = {}
			data = {'notes': request.POST.get('notes')}
			
			tittle = request.POST.get('tittle', '').strip()
			if not tittle:
				errors['tittle'] = u"Назва предмету є обов'язковою"
			else:
				data['tittle'] = tittle

			examtime = request.POST.get('examtime', '').strip()
			try:
				datetime.strptime(examtime, '%Y-%m-%d')
			except Exception:
				errors['examtime'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
			else:
				data['examtime'] = examtime


			teach = request.POST.get('teach', '').strip()
			if not teach:
				errors['teach'] = u"Викладач є обов'язковим полем"
			else:
				data['teach'] = tittle

			exam_group = request.POST.get('exam_group', '').strip()
			if not exam_group:
				errors['exam_group'] = u"Оберіть групу для іспиту"
			else:
				if len(Group.objects.all().filter(id=exam_group)) != 1:
					errors['exam_group'] = u"Оберіть коректну групу для іспиту"
				else:
					data['exam_group'] = Group.objects.get(pk=exam_group)

			if not errors:
				exam = Exam(**data)
				exam.save()
				# redirect to students list
				messages.success(request, u'Іспит успішно доданий!')
				return HttpResponseRedirect(reverse('exams'))
			else:
				# render form with errors and previous user input
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')
				return render(request, 'students/exams_add.html',
						{'groups': Group.objects.all().order_by('tittle'),
							'errors': errors})

		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			messages.info(request, u'Додавання іспиту скасовано!')
			#return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
			return HttpResponseRedirect(reverse('exams'))
	
	else:
		# initial form render
		return render(request, 'students/exams_add.html',
			{'groups': Group.objects.all().order_by('tittle')})


def exams_edit(request, eid):
	current_exam = Exam.objects.get(id=eid)
	# was form posted?
	if request.method == "POST":
		if request.POST.get('add_button') is not None:
			
			errors = {}

			current_exam.tittle = request.POST.get('tittle', '').strip() 
			if not current_exam.tittle:
				errors['tittle'] = u"Назва предмету є обов'язковою"

			examtime = request.POST.get('examtime', '').strip()
			try:
				datetime.strptime(examtime, u'%Y-%m-%d')
			except Exception:
				errors['examtime'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
			else:
				current_exam.examtime = examtime

			current_exam.teach = request.POST.get('teach', '').strip() 
			if not current_exam.teach:
				errors['teach'] = u"Викладач є обов'язковим полем"

			exam_group = request.POST.get('exam_group', '').strip()
			if not exam_group:
				errors['exam_group'] = u"Оберіть групу для іспиту"
			else:
				if len(Group.objects.all().filter(id=exam_group)) != 1:
					errors['exam_group'] = u"Оберіть коректну групу для іспиту"
				else:
					current_exam.exam_group = Group.objects.get(pk=exam_group)

			current_exam.notes = request.POST.get('notes', '').strip() 

			if not errors:
				current_exam.save()
				# redirect to students list
				messages.success(request, u'Іспит успішно редаговано!')
				return HttpResponseRedirect(reverse('exams'))
			else:
				# render form with errors and previous user input
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')
				return render(request, 'students/exams_edit.html',
						{'groups': Group.objects.all().order_by('tittle'),
							'errors': errors, 'current_exam': Exam.objects.get(id=eid)})


		else:
			# redirect to home page on cancel button
			messages.info(request, u'Редагування іспиту скасовано!')
			return HttpResponseRedirect(reverse('exams'))
	else:
		# initial form render
		return render(request, 'students/exams_edit.html',
			{'groups': Group.objects.all().order_by('tittle'), 'current_exam': current_exam, 
				'date': current_exam.examtime.strftime('%Y-%m-%d')})


def exams_delete(request, eid):
	current_exam = Exam.objects.get(id=eid)
	#was form posted?
	if request.method == "POST":
		#pressed delete_button
		if request.POST.get('delete_button') is not None:
			current_exam.delete()
			messages.success(request, u'Іспит успішно видалено!')
			return HttpResponseRedirect(reverse('exams'))
		#pressed cancel_button
		else:
			# redirect to home page on cancel button
			messages.info(request, u'Редагування іспиту скасовано!')
			return HttpResponseRedirect(reverse('exams'))

	else:
		return render(request, 'students/exams_confirm_delete.html', {'current_exam': current_exam})
	