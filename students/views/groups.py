# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group

def groups_list(request):
  groups = Group.objects.all()
  groups = groups.order_by('tittle')
  # try to order groups list
  order_by = request.GET.get('order_by', 'tittle')
  if order_by in ('tittle', 'leader'):
    groups = groups.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
      groups = groups.reverse()

  n = 3
  paginator = Paginator(groups, n)
  page = request.GET.get('page', '1')
  try:
    groups = paginator.page(page)
  except PageNotAnInteger:
    # If page is not an integer, deliver first page.
    groups = paginator.page(1)
  except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
    groups = paginator.page(paginator.num_pages)

  numbs=[]
  for i in range(n):
    numbs.append((int(page)-1)*n+i+1)

  return render(request, 'students/groups_list.html', {'groups':groups, 'numbs':numbs})



class GroupForm(ModelForm):
  class Meta:
    model = Group
    fields = ['tittle', 'leader', 'notes']
  def __init__(self, *args, **kwargs):
    super(GroupForm, self).__init__(*args, **kwargs)
    # this helper object allows us to customize form
    self.helper = FormHelper(self)
    # form tag attributes
    #self.helper.form_action = reverse('groups_add')
    self.helper.form_method = 'POST'
    self.helper.form_class = 'form-horizontal'
    # set form field properties
    self.helper.help_text_inline = True
    self.helper.label_class = 'col-sm-2 control-label'
    self.helper.field_class = 'col-sm-10'
    # add buttons
    self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
    self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))
    #self.helper.add_input(Button('cancel_button', 'Cancel', css_class='btn-default', onclick="window.history.back()"))



class GroupCreateView(CreateView):
  model = Group
  template_name = 'students/groups_add.html'
  form_class = GroupForm

  def get_success_url(self):
    return reverse('groups')

  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      messages.info(request, u'Додавання групи скасовано!')
      return HttpResponseRedirect(reverse('groups'))
    elif request.POST.get('add_button'):
      if GroupForm(request.POST).is_valid():
        messages.success(request, u'Додавання групи %s пройшло успішно!' %request.POST.get('tittle'))

      return super(GroupCreateView, self).post(request, *args, **kwargs)


class GroupUpdateView(UpdateView):
  model = Group
  template_name = 'students/groups_edit.html'
  form_class = GroupForm

  def get_success_url(self):
    return reverse('groups')

  def post(self, request, *args, **kwargs):
    if request.POST.get('cancel_button'):
      messages.info(request, u'Редагування групи скасовано!')
      return HttpResponseRedirect(reverse('groups'))
    elif request.POST.get('add_button'):
      if GroupForm(request.POST).is_valid():
        messages.success(request, u'Редагування групи пройшло успішно!')

      return super(GroupUpdateView, self).post(request, *args, **kwargs)



def groups_edit(request, gid):
  return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
  return HttpResponse('<h1>Delete Group %s</h1>' % gid)