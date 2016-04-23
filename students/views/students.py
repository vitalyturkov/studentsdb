# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.forms import ModelForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from crispy_forms.bootstrap import FieldWithButtons, StrictButton

import re

from ..models.students import Student
from ..models.groups import Group

from ..util import paginate, get_current_group


def students_list(request):

	current_group = get_current_group(request)
	if current_group:
		students = Student.objects.filter(student_group=current_group)
	else:
		# otherwise show all students
		students = Student.objects.all()
	# try to order students list
	order_by = request.GET.get('order_by', 'last_name')
	if order_by in ('last_name', 'first_name', 'ticket'):
		students = students.order_by(order_by)
		if request.GET.get('reverse', '') == '1':
			students = students.reverse()


	


	
	n = 5
	# apply pagination, 5 students per page
	context = paginate(students, n, request, {},
		var_name='students')
	
	"""	
	n = request.GET.get('page', '1')

	students = students[0:int(n)*5]
	"""

	return render(request, 'students/students_list.html',
		context)


class StudentForm(ModelForm):
	class Meta:
		model = Student
		fields = ['first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes']
	
	def __init__(self, *args, **kwargs):
	# call original initializator
		super(StudentForm, self).__init__(*args, **kwargs)
		# this helper object allows us to customize form
		self.helper = FormHelper(self)
		# form tag attributes
		#<span class="input-group-addon">
         #   <span class="glyphicon glyphicon-calendar"></span>
        #</span>
		#self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		# set form field properties
		self.helper.help_text_inline = True
		#self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		self.helper.layout = Layout(
			Field('first_name', placeholder=u"Ім'я студента"),
			Field('last_name', placeholder=u"Прізвище студента"),
			Field('middle_name', placeholder=u"Ім'я по-батькові студента"),
			FieldWithButtons('birthday', StrictButton('<span class="glyphicon glyphicon-calendar"></span>', id='calend')),
			#Field('birthday', placeholder=u"Ваш день народження"),
			Field('photo'),
			Field('ticket', placeholder=u"Номер студентського квитка"),
			Field('student_group'),
			Field('notes', placeholder=u"Додаткові нотатки")
			)

		#ordering field 'student_group' at form by tittle
		self.fields['student_group'].queryset = Group.objects.order_by('tittle')
		
		# add buttons
		self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))



class StudentCreateView(CreateView):
	model = Student
	template_name = 'students/students_add.html'
	form_class = StudentForm

	def get_success_url(self):
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
		else:
			if StudentForm(request.POST).is_valid():
				messages.success(request, u'Додавання студента %s %s пройшло успішно!' 
					%(request.POST.get('first_name'), request.POST.get('last_name')))
			else:
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')

			return super(StudentCreateView, self).post(request, *args, **kwargs)

class StudentUpdateView(UpdateView):
	model = Student
	template_name = 'students/students_edit.html'
	form_class = StudentForm

	def get_success_url(self):
		return reverse('home')


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if request.POST.get('cancel_button'):
			messages.info(request, u'Редагування студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
		else:
			if form.is_valid():
				group = Group.objects.filter(leader=kwargs['pk'])
			
				if len(group) > 0 and group[0] != Group.objects.get(id=request.POST.get('student_group')):
					messages.warning(request, u'Студент є старостою іншої групи!')
					form.add_error('student_group', 'Група не може бути зміненою')
					return render(request, self.template_name, {'form': form})
				messages.success(request, u'Редагування студента пройшло успішно!')
			else:
				messages.warning(request, u'Будь-ласка, виправте наступні помилки!')
			return super(StudentUpdateView, self).post(request, *args, **kwargs)
		
class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'
	def get_success_url(self):
		return reverse('home')

	def post(self, request, *args, **kwargs):	
		if request.POST.get('cancel_button'):
			messages.info(request, u'Видалення студента скасовано!')
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.success(request, u'Видалення студента пройшло успішно!')
			return super(StudentDeleteView, self).post(request, *args, **kwargs)



#its part of code just at list and Django doesnt work with it
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