# -*- coding: utf-8 -*-

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models.students import Student
from .models.groups import Group
from .models.exams import Exam
from .models.monthjournal import MonthJournal

from django.http import HttpResponse, HttpResponseRedirect

class StudentFormAdmin(ModelForm):
	def clean_student_group(self):
		"""Check if student is leader in any group.
		If yes, then ensure it's the same as selected group."""
		# get group where current student is a leader
		groups = Group.objects.filter(leader=self.instance)
		if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
			raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')
		return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
	form = StudentFormAdmin
	
	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})


class GroupFormAdmin(ModelForm):
	def clean_leader(self):
		"""Check if student belongs to editing group"""
		if self.cleaned_data['leader'] and self.cleaned_data['leader'].student_group != self.instance:
			raise ValidationError(u'Студент належить до іншої групи.', code='invalid')
		return self.cleaned_data['leader']

class GroupAdmin(admin.ModelAdmin):
	list_display = ['tittle', 'leader']
	list_display_links = ['tittle']
	list_editable = ['leader']
	ordering = ['tittle']
	list_filter = ['leader']
	list_per_page = 10
	search_fields = ['tittle', 'notes']
	form = GroupFormAdmin

	def view_on_site(self, obj):
		return reverse('groups_edit', kwargs={'pk': obj.id})	


class ExamAdmin(admin.ModelAdmin):
	list_display = ['tittle', 'examtime', 'teach', 'exam_group']
	list_display_links = ['tittle', 'examtime', 'teach']
	list_editable = ['exam_group']
	ordering = ['tittle']
	list_filter = ['exam_group']
	list_per_page = 10
	search_fields = ['tittle', 'examtime', 'teach', 'notes']

	"""
	!Problem with view_on_site, because view exams_edit isn't class!

	def view_on_site(self, obj):
		return reverse('exams_edit', {'pk':obj.id})
	"""

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(MonthJournal)
