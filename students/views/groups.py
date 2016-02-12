# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def groups_add(request):
  return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
  return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
  return HttpResponse('<h1>Delete Group %s</h1>' % gid)