# -*- coding: utf-8 -*-
from django.db import models


class Exam(models.Model):

	class Meta(object):
		verbose_name = u"Іспит"
		verbose_name_plural = u"Іспити"
	
	tittle = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Назва предмету")

	examtime = models.DateField(
		blank=False,
		verbose_name=u"Дата і час проведення іспиту",
		null=True)
	
	teach = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Викладач")

	exam_group = models.ForeignKey('Group',
		verbose_name=u"Група",
		blank=False,
		null=True,
		on_delete=models.PROTECT)

	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки, щодо іспиту")
	
	def __unicode__(self):
		return u"%s - %s" % (self.tittle, self.exam_group)