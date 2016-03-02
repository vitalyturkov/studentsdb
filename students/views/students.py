# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import UpdateView
from django.forms import ModelForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

import re

from ..models.students import Student
from ..models.groups import Group



def students_list(request):
	students = Student.objects.all()
	# try to order students list
	order_by = request.GET.get('order_by', 'last_name')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()

	n = 5
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
		{'students': students, 'numbs': numbs})



def students_add(request):
	# was form posted?
	if request.method == "POST":
		# was form add button clicked?
		if request.POST.get('add_button') is not None:
			# TODO: validate input from user
		
			# errors collection
			errors = {}
			# validate student data will go here
			data = {'middle_name': request.POST.get('middle_name'),
			'notes': request.POST.get('notes')}
			# validate user input
			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім'я є обов'язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов'язковим"
			else:
				data['last_name'] = last_name

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов'язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу для студента"
			else:
				if len(Group.objects.filter(pk=student_group)) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = Group.objects.get(pk=student_group)

			photo = request.FILES.get('photo')
	
			if photo:
				
				if re.findall(r'.jpeg$', photo.name.lower()) or re.findall(r'.jpg$', photo.name.lower()) or re.findall(r'.png$', photo.name.lower()):
					if photo.size <= 2097152:
						data['photo'] = photo
					else:
						errors['photo'] = u"Занадто великий розмір фото"
				else:
					errors['photo'] = u"Некоректний формат фото"

			# save student
			if not errors:
				student = Student(**data)
				student.save()
				# redirect to students list

				#return HttpResponseRedirect(u'%s?status_message=Студент %s %s успішно доданий!' %(reverse('home'), student.first_name, student.last_name))
				messages.success(request, u'Студент %s %s успішно доданий!' %(student.first_name, student.last_name))
				return HttpResponseRedirect(reverse('home'))

			else:
				# render form with errors and previous user input
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')
				return render(request, 'students/students_add.html',
						{'groups': Group.objects.all().order_by('tittle'),
							'errors': errors})

		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			messages.info(request, u'Додавання студента скасовано!')
			#return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
			return HttpResponseRedirect(reverse('home'))
	else:
		# initial form render
		return render(request, 'students/students_add.html',
			{'groups': Group.objects.all().order_by('tittle')})


class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes']
	def __init__(self, *args, **kwargs):
	# call original initializator
		super(StudentUpdateForm, self).__init__(*args, **kwargs)
		# this helper object allows us to customize form
		self.helper = FormHelper(self)
		# form tag attributes
		
		#self.helper.form_action = reverse_lazy('students_edit', kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		# set form field properties
		self.helper.help_text_inline = True
		#self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# add buttons
		self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))
		#self.helper.layout[-1] = FormActions(
		#Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
		#Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),)

		"""
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('home')
		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# form buttons
		self.helper.add_input(Submit('send_button', u'Надіслати'))
		"""
	

class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentUpdateForm

	def get_success_url(self):
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
		else:
			if StudentUpdateForm(request.POST).is_valid():
				messages.success(request, u'Редагування студента пройшло успішно!')
			else:
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')

			return super(StudentUpdateView, self).post(request, *args, **kwargs)
		
			


def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)