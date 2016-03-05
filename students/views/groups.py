# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms import ModelForm
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

from ..models.groups import Group
from ..models.students import Student


def groups_list(request):
  groups = Group.objects.all()
  groups = groups.order_by('tittle')
  # try to order groups list
  order_by = request.GET.get('order_by', 'tittle')
  if order_by in ('tittle', 'leader'):
    groups = groups.order_by(order_by)
    if request.GET.get('reverse', '') == '1':
      groups = groups.reverse()

  n = 5
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

    self.helper.layout = Layout(
      Field('tittle', placeholder=u"Назва групи"),
      Field('leader'),
      Field('notes', placeholder=u"Додаткові нотатки")
      )
    # add buttons
    self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
    self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link"))


class GroupCreateView(CreateView):
  model = Group
  template_name = 'students/groups_add.html'
  form_class = GroupForm
 
  def get_success_url(self):
    return reverse('groups')

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if request.POST.get('cancel_button'):
      messages.info(request, u'Додавання групи скасовано!')
      return HttpResponseRedirect(reverse('groups'))
    elif request.POST.get('add_button'):
      if form.is_valid():
        if request.POST.get('leader'):
          messages.warning(request, u'Студент %s не може бути старостою новострореної групи, бо він належить до іншої групи!' %Student.objects.get(id=request.POST.get('leader')))
          return render(request, self.template_name, {'form': form})
        messages.success(request, u'Додавання групи %s пройшло успішно!' %request.POST.get('tittle'))
      else:
        messages.warning(request, u'Будь-ласка, виправте наступні помилки!')
      return super(GroupCreateView, self).post(request, *args, **kwargs)


class GroupUpdateView(UpdateView):
  model = Group
  template_name = 'students/groups_edit.html'
  form_class = GroupForm

  def get_success_url(self):
    return reverse('groups')

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)

    if request.POST.get('cancel_button'):
      messages.info(request, u'Редагування групи скасовано!')
      return HttpResponseRedirect(reverse('groups'))
   
    else:
     
      if request.POST.get('leader'): 
        if Student.objects.get(id=request.POST.get('leader')).student_group != Group.objects.get(id=kwargs['pk']):
          messages.warning(request, u'Студент %s не належить до групи %s' 
            %(Student.objects.get(id=request.POST.get('leader')), request.POST.get('tittle')))
          return render(request, self.template_name, {'form': form})
      
      if form.is_valid():
        messages.success(request, u'Редагування групи пройшло успішно!')
     
      else:
        if request.POST.get('leader') and request.POST.get('tittle'):
          if Student.objects.get(id=request.POST.get('leader')) == Group.objects.get(id=kwargs['pk']).leader:
            messages.success(request, u'Редагування групи пройшло успішно!') 
        else:
          messages.warning(request, u'Будь-ласка, виправте наступні помилки!')

      return super(GroupUpdateView, self).post(request, *args, **kwargs)


class GroupDeleteView(DeleteView):
  model = Group
  template_name = 'students/groups_confirm_delete.html'
  
  def get_success_url(self):
    return reverse('groups')
  
  def post(self, request, *args, **kwargs): 
    if request.POST.get('cancel_button'):
      messages.info(request, u'Видалення групи скасовано!')
      return HttpResponseRedirect(reverse('groups'))
   
    else: 
      try:
        super(GroupDeleteView, self).post(request, *args, **kwargs)
      
      except Exception:
        messages.warning(request, u"Група не може бути видалена, спочатку видаліть об'єкти, які пов'язані з цією групою" )
        return render(request, 'students/groups_confirm_delete.html', 
          {'del_id': kwargs['pk'], 'del_group': Group.objects.get(id=kwargs['pk'])})
    
      else:
        messages.success(request, u'Видалення групи пройшло успішно!')
        return HttpResponseRedirect(reverse('groups'))
